
# chunking/chunk_trace_builder.py

from datetime import datetime
from db.mongo_client import trace_collection


def log_query_trace(query: str, matches: list):
    """
    Save query ↔️ matched chunks trace.
    """
    trace_entry = {
        "query": query,
        "matched_chunks": matches,
        "timestamp": datetime.utcnow()
    }
    result = trace_collection.insert_one(trace_entry)
    return str(result.inserted_id)
