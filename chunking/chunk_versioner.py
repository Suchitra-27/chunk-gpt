# chunking/chunk_versioner.py

from db.mongo_client import patch_collection
from datetime import datetime

def save_patch_version(chunk_id: str, original: str, patched: str):
    version = {
        "chunk_id": chunk_id,
        "original": original,
        "patched": patched,
        "timestamp": datetime.utcnow()
    }
    result = patch_collection.insert_one(version)
    version["_id"] = str(result.inserted_id)
    return version


def approve_patch(chunk_id: str):
    latest_patch = patch_collection.find_one({"chunk_id": chunk_id}, sort=[("timestamp", -1)])
    if not latest_patch:
        return {"error": "No patch found for this chunk_id"}
    
    return {
        "chunk_id": chunk_id,
        "original": latest_patch["original"],
        "patched": latest_patch["patched"]
    }
