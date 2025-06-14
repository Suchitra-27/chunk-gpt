import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.mongo_client import feedback_collection, trace_collection


feedback_collection.delete_many({})
trace_collection.delete_many({})
# patch_collection.delete_many({})

print("✅ MongoDB collections cleared.")
