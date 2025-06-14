import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["chunk_gpt"]

feedback_collection = db["feedback"]
patch_collection = db["patches"]
trace_collection = db["trace_logs"]
decay_collection = db["decay_meta"]
trace_collection = db["chunk_traces"]
