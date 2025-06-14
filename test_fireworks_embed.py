# test_fireworks_embed.py

from dotenv import load_dotenv
load_dotenv()

import os
from embedding.embedder import embed_text

print("Loaded API Key:", os.getenv("FIREWORKS_API_KEY"))  # Debug print

sample_text = "Artificial intelligence is transforming the world."

try:
    vector = embed_text(sample_text)
    print(f"✅ Embedding successful! First 5 dimensions:\n{vector[:5]}")
except Exception as e:
    print(f"❌ Embedding failed: {e}")
