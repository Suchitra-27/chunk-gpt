# mock_ragie_server.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict
import uvicorn

app = FastAPI(title="Mock Ragie Receiver")

class ChunkRecord(BaseModel):
    chunk_id: str
    chunk_text: str
    embedding: List[float]
    metadata: Dict[str, str]

@app.post("/upload")
async def receive_embedding(chunk: ChunkRecord):
    print("\n✅ Chunk received by mock Ragie:")
    print(f"ID: {chunk.chunk_id}")
    print(f"Source: {chunk.metadata.get('source')}")
    print(f"First 5 values of embedding: {chunk.embedding[:5]}")
    return {"status": "stored", "chunk_id": chunk.chunk_id}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
