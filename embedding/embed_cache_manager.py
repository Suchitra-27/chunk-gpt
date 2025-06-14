# embedding/embed_cache_manager.py

import hashlib
import os
import json

CACHE_FILE = "embed_cache.json"

# Load or initialize cache
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        cache = json.load(f)
else:
    cache = {}

def get_text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def is_already_embedded(text: str) -> bool:
    hash_val = get_text_hash(text)
    return hash_val in cache

def get_cached_embedding(text: str):
    return cache.get(get_text_hash(text))

def store_embedding(text: str, embedding: list):
    hash_val = get_text_hash(text)
    cache[hash_val] = embedding
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)
