# utils/tokenizer.py

import tiktoken

# Default tokenizer for OpenAI GPT-3.5/4
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def count_tokens(text: str) -> int:
    return len(encoding.encode(text))

def truncate_text_by_tokens(text: str, max_tokens: int) -> str:
    tokens = encoding.encode(text)
    truncated = tokens[:max_tokens]
    return encoding.decode(truncated)
