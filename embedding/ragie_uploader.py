import os
import uuid
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

# pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
# index = pc.Index(os.getenv("PINECONE_INDEX"))

# # 🚨 Delete everything
# index.delete(delete_all=True)
# print("✅ Pinecone index cleared.")


# Initialize Pinecone client (v3 SDK)
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

def save_to_ragie(chunk_text, embedding, metadata={}):
    chunk_id = str(uuid.uuid4())

    metadata = metadata or {}
    metadata["text"] = chunk_text[:200]  # Trim metadata

    index.upsert([
        {
            "id": chunk_id,
            "values": embedding,
            "metadata": metadata
        }
    ])

    return chunk_id
