from core.ingestion.ingestion import ingest_pdf
from core.embeddings.embedding import embed_chunks

def index_book(id: str, pdf_path: str):
    print(f"[INDEX] Starting indexing for: {id}")
    print(f"[INDEX] PDF path: {pdf_path}")

    chunks = ingest_pdf(pdf_path, r"data/report")
    embed_chunks(chunks, f"data/index/{id}")

    print(f"[INDEX] Finished indexing for: {id}")
