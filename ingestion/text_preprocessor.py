
# ingestion/text_preprocessor.py

import re

def clean_text(raw_text: str) -> str:
    text = raw_text.strip()
    
    # Normalize whitespace and newlines
    text = re.sub(r'\s+', ' ', text)

    # Replace fancy quotes/dashes
    text = text.replace("“", "\"").replace("”", "\"")
    text = text.replace("‘", "'").replace("’", "'")
    text = text.replace("–", "-").replace("—", "-")

    # Optional: remove non-printable chars
    text = re.sub(r'[^\x20-\x7E]', '', text)

    return text
