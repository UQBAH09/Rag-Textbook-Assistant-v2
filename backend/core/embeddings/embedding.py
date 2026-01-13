from core.embeddings.embedding_config import configure_llamaindex_embeddings
from core.embeddings.loader import load_chunks_as_documents
from core.index.indexer import build_and_persist_index

def embed_chunks(chunks: list[dict], persist_dir: str):
    configure_llamaindex_embeddings()
    documents = load_chunks_as_documents(chunks)
    build_and_persist_index(documents, persist_dir)
