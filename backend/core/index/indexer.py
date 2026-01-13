from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.faiss import FaissVectorStore
import faiss
import os


def build_and_persist_index(documents, persist_dir: str):
    os.makedirs(persist_dir, exist_ok=True)

    dim = 768  # nomic-embed-text
    faiss_index = faiss.IndexFlatL2(dim)

    vector_store = FaissVectorStore(faiss_index=faiss_index)

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True
    )

    # ✅ Persist metadata (docstore, index_store, etc.)
    storage_context.persist(persist_dir)

    # ✅ Persist FAISS index explicitly
    faiss.write_index(
        faiss_index,
        os.path.join(persist_dir, "faiss.index")
    )

    return index
