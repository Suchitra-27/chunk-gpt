import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_community.embeddings import HuggingFaceEmbeddings
from chunking.chunk_versioner import save_patch_version

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)


def suggest_patch(chunk_id: str):
    # 🔍 Try to fetch chunk from Pinecone
    response = index.fetch(ids=[chunk_id])

    if chunk_id not in response.vectors:
        return {"error": f"Chunk ID {chunk_id} not found."}

    # ✅ New access pattern using `.vectors[chunk_id].metadata`
    metadata = response.vectors[chunk_id].metadata or {}
    chunk_text = metadata.get("text")

    if not chunk_text:
        return {"error": "No text found in metadata for this chunk."}

    patched = "Summary: " + chunk_text[:200]
    return save_patch_version(chunk_id, chunk_text, patched)

