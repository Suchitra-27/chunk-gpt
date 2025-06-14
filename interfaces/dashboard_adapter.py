
# interfaces/dashboard_adapter.py

from db.mongo_client import feedback_collection, patch_collection
from fastapi import APIRouter

router = APIRouter()

@router.get("/dashboard/feedback")
def list_feedback():
    return list(feedback_collection.find({}, {"_id": 0}))

@router.get("/dashboard/patches")
def list_patches():
    return list(patch_collection.find({}, {"_id": 0}))
