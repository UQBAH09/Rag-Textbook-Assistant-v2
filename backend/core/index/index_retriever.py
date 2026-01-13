from pathlib import Path
import os
import faiss

from llama_index.core import StorageContext, load_index_from_storage, VectorStoreIndex
from llama_index.vector_stores.faiss import FaissVectorStore


def load_index(persist_dir: str) -> VectorStoreIndex:
    persist_path = Path(persist_dir)

    if not persist_path.exists():
        raise FileNotFoundError(
            f"Index directory not found: {persist_dir}. "
            "Have you built the index?"
        )

    faiss_path = persist_path / "faiss.index"

    if not faiss_path.exists():
        raise FileNotFoundError(
            f"FAISS index not found at {faiss_path}"
        )

    # ✅ Load FAISS binary index explicitly
    faiss_index = faiss.read_index(str(faiss_path))

    # ✅ Inject FAISS index into vector store
    vector_store = FaissVectorStore(faiss_index=faiss_index)

    # ✅ Tell LlamaIndex to use this vector store
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store,
        persist_dir=str(persist_dir)
    )

    return load_index_from_storage(storage_context)
