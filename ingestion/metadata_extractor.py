
# ingestion/metadata_extractor.py

import os
from langdetect import detect

def extract_file_metadata(filename: str, content: str) -> dict:
    file_type = os.path.splitext(filename)[1].lower().replace('.', '')

    try:
        language = detect(content)
    except:
        language = "unknown"

    return {
        "file_type": file_type,
        "language": language
    }
