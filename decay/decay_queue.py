
# decay/decay_queue.py

from fastapi import APIRouter
from decay.decay_analyzer import analyze_decay

router = APIRouter()

@router.get("/decay-queue")
def get_decay_queue():
    result = analyze_decay()
    return {
        "decay_candidates": result["decayed_chunks"],
        "count": result["count"],
        "total_chunks": result["total"]
    }
