# feedback/feedback_handler.py

from db.mongo_client import feedback_collection
from datetime import datetime

def save_feedback(chunk_id: str, feedback: str, notes: str = ""):
    entry = {
        "chunk_id": chunk_id,
        "feedback": feedback,
        "notes": notes,
        "timestamp": datetime.utcnow()
    }
    
    result = feedback_collection.insert_one(entry)
    entry["_id"] = str(result.inserted_id)
    return entry

