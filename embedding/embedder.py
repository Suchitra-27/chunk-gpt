from langchain_community.embeddings import HuggingFaceEmbeddings

# Load the embedding model (BGE-small)
embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)

from embedding.embed_cache_manager import (
    is_already_embedded,
    get_cached_embedding,
    store_embedding
)


def embed_text(text: str):
    if is_already_embedded(text):
        return get_cached_embedding(text)

    embedding = embedding_model.embed_query(text)
    store_embedding(text, embedding)
    return embedding

