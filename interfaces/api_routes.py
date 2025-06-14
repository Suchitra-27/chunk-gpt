import os
import json
from fastapi import APIRouter, UploadFile, File, Body, Query
from typing import List
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone

# === Load .env + Pinecone setup ===
load_dotenv()
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)

# === Module imports ===
from ingestion.file_loader import extract_text_from_file
from ingestion.text_preprocessor import clean_text
from ingestion.metadata_extractor import extract_file_metadata

from chunking.chunker import split_text_into_chunks
from chunking.chunk_versioner import approve_patch
from chunking.chunk_trace_builder import log_query_trace

from embedding.embedder import embed_text
from embedding.ragie_uploader import save_to_ragie

from embedding.embed_cache_manager import (
    is_already_embedded,
    get_cached_embedding,
    store_embedding
)

from feedback.feedback_handler import save_feedback
from feedback.patch_suggester import suggest_patch

from pydantic import BaseModel

router = APIRouter()

# === Upload & Ingest ===
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    extracted_text = extract_text_from_file(file.filename, content)
    cleaned_text = clean_text(extracted_text)
    chunks = split_text_into_chunks(cleaned_text)

    stored_chunk_ids = []
    for chunk in chunks:
        if is_already_embedded(chunk):
            vector = get_cached_embedding(chunk)
        else:
            vector = embed_text(chunk)
            store_embedding(chunk, vector)

        metadata = extract_file_metadata(file.filename, chunk)
        metadata["source"] = file.filename

        chunk_id = save_to_ragie(chunk, vector, metadata)
        if chunk_id:
            stored_chunk_ids.append(chunk_id)

    return {
        "status": "done",
        "chunks_uploaded": len(stored_chunk_ids),
        "first_chunk_id": stored_chunk_ids[0] if stored_chunk_ids else None
    }

# === Semantic Query + Trace Log ===
@router.post("/query")
def search_chunks(question: str = Body(..., embed=True)):
    query_embed = embedding_model.embed_query(question)
    results = index.query(vector=query_embed, top_k=3, include_metadata=True)

    matches = []
    for match in results.matches:
        matches.append({
            "score": match.score,
            "chunk_id": match.id,
            "text_snippet": match.metadata.get("text", "[no content]")
        })

    # log_query_trace(question, matches)

    return {
        "question": question,
        "matches": matches
    }

# === Feedback API ===
class FeedbackInput(BaseModel):
    chunk_id: str
    feedback: str  # "upvote" or "downvote"
    notes: str = ""

@router.post("/feedback")
def collect_feedback(feedback: FeedbackInput):
    entry = save_feedback(feedback.chunk_id, feedback.feedback, feedback.notes)
    return {"status": "saved", "entry": entry}

# === Patch Suggestion ===
@router.get("/patch")
def generate_patch(chunk_id: str = Query(...)):
    result = suggest_patch(chunk_id)
    return result

# === Patch Approval ===
@router.post("/approve-patch")
def approve(chunk_id: str = Query(...)):
    return approve_patch(chunk_id)

# === Decay Analyzer Report ===
from decay.decay_analyzer import analyze_decay

@router.get("/decay-report")
def decay_report():
    return analyze_decay()

# === Decay Queue Router ===
from decay.decay_queue import router as decay_router
router.include_router(decay_router)

# === Dashboard Viewer (optional) ===
from interfaces.dashboard_adapter import router as dashboard_router
router.include_router(dashboard_router)
