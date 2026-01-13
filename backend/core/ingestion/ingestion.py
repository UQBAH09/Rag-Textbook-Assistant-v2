from pathlib import Path
from typing import Dict, Any

from core.ingestion.loader import load_pdf_pages
from core.ingestion.parser import parse_structure
from core.ingestion.chunker import chunk_sections
from core.ingestion.validator import validate_chunks

from core.utils.utils import (
    save_pages_to_json,
    load_pages_from_json,
    save_chapters_with_sections_to_json,
    load_chapters_with_sections_from_json,
    save_chunks_to_json,
    load_chunks_from_json,
    save_validation_report,
)


def ingest_pdf(
    pdf_path: str,
    output_dir: str = "data/ingestion",
    debug: bool = False
) -> Dict[str, Any]:
    """
    Full ingestion pipeline:
    PDF -> pages -> chapters & sections -> chunks -> validation report

    Returns:
        dict with paths to generated artifacts
    """

    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    book_id = pdf_path.stem

    # -----------------------------
    # Stage 1A: Load PDF pages
    # -----------------------------
    pages = load_pdf_pages(str(pdf_path))

    if debug:
        save_pages_to_json(pages, output_dir / f"{book_id}_pages.json")

    # -----------------------------
    # Stage 1B: Parse structure
    # -----------------------------
    chapters = parse_structure(pages)

    if debug:
        save_chapters_with_sections_to_json(
            chapters,
            output_dir / f"{book_id}_chapters.json"
        )

    # -----------------------------
    # Stage 1C: Chunking
    # -----------------------------
    chunks = chunk_sections(chapters, book_id=book_id)

    if debug:
        chunks_path = output_dir / f"{book_id}_chunks.json"
        save_chunks_to_json(chunks, chunks_path)

    # -----------------------------
    # Stage 1D: Validation
    # -----------------------------
    report = validate_chunks(chunks)

    report_path = output_dir / f"{book_id}_validation.json"
    save_validation_report(report, report_path)

    return chunks
