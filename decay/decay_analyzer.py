# decay/decay_analyzer.py

from datetime import datetime, timedelta
from db.mongo_client import trace_collection, feedback_collection
from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

DECAY_THRESHOLD_DAYS = 7  # Mark if unused for over 7 days

def get_all_chunk_ids():
    stats = index.describe_index_stats()
    return stats["total_vector_count"], list(stats["namespaces"].get("", {}).get("vectors", {}).keys())

def analyze_decay():
    total, chunk_ids = get_all_chunk_ids()

    now = datetime.utcnow()
    threshold_time = now - timedelta(days=DECAY_THRESHOLD_DAYS)

    decayed = []

    for chunk_id in chunk_ids:
        # Check last feedback or query trace
        trace = trace_collection.find_one({"matched_chunks.chunk_id": chunk_id}, sort=[("timestamp", -1)])
        feedback = feedback_collection.find_one({"chunk_id": chunk_id}, sort=[("timestamp", -1)])

        latest_time = None
        if trace and "timestamp" in trace:
            latest_time = trace["timestamp"]
        if feedback and "timestamp" in feedback:
            if not latest_time or feedback["timestamp"] > latest_time:
                latest_time = feedback["timestamp"]

        if not latest_time or latest_time < threshold_time:
            decayed.append(chunk_id)

    return {"decayed_chunks": decayed, "count": len(decayed), "total": total}
