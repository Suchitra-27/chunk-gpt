# chunk_gpt/chunking/chunker.py

import tiktoken

def split_text_into_chunks(text: str, max_tokens: int = 300, overlap: int = 50):
    tokenizer = tiktoken.get_encoding("cl100k_base")  # Same as used by OpenAI/BGE
    tokens = tokenizer.encode(text)

    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunk_tokens = tokens[start:end]
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)
        start += max_tokens - overlap  # Move window with overlap

    return chunks
