import json
from typing import List, Dict, Any


def save_pages_to_json(
    pages: List[Dict],
    output_path: str,
    pretty: bool = True
) -> None:
    """
    Save raw PDF pages (Stage 1A) to JSON for inspection.

    Each entry contains:
    - page_number
    - text
    """
    with open(output_path, "w", encoding="utf-8") as f:
        if pretty:
            json.dump(pages, f, indent=2, ensure_ascii=False)
        else:
            json.dump(pages, f, ensure_ascii=False)


def save_chapters_to_json(
    chapters: List[Dict],
    output_path: str,
    pretty: bool = True
) -> None:
    """
    Save parsed chapters and sections (Stage 1B) to JSON for inspection.

    Structure:
    - chapter_number
    - chapter_name
    - sections[]
        - section_number
        - section_name
        - page_start
        - page_end
        - text
    """
    with open(output_path, "w", encoding="utf-8") as f:
        if pretty:
            json.dump(chapters, f, indent=2, ensure_ascii=False)
        else:
            json.dump(chapters, f, ensure_ascii=False)

def load_chapters_from_json(json_path: str) -> List[Dict]:
    """
    Load chapters from a JSON file.

    The JSON must contain a list of chapter objects with:
    - chapter_number (int)
    - chapter_name (str)
    - page_start (int)
    - page_end (int)
    - text (str)

    Args:
        json_path (str): Path to chapters JSON file.

    Returns:
        List[Dict]: List of chapter dictionaries.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        chapters = json.load(f)

    # Basic validation
    for ch in chapters:
        required_fields = [
            "chapter_number",
            "chapter_name",
            "page_start",
            "page_end",
            "text"
        ]

        for field in required_fields:
            if field not in ch:
                raise ValueError(f"Missing field '{field}' in chapter JSON")

        if not isinstance(ch["chapter_number"], int):
            raise TypeError("chapter_number must be int")

        if not isinstance(ch["text"], str):
            raise TypeError("text must be str")

    return chapters

def save_chunks_to_json(
    chunks: List[Dict],
    output_path: str,
    pretty: bool = True
) -> None:
    """
    Save final enriched chunks (Stage 1C + 1D) to JSON for inspection.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        if pretty:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        else:
            json.dump(chunks, f, ensure_ascii=False)

def load_chunks_from_json(
    input_path: str
) -> List[Dict]:
    """
    Load chunk data from a JSON file.
    """
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_pages_from_json(json_path: str) -> List[Dict]:
    """
    Load PDF pages from a previously saved JSON file.

    The JSON must contain a list of objects with:
    - page_number (int)
    - text (str)

    Args:
        json_path (str): Path to pages.json

    Returns:
        List[Dict]: Pages in the same format as load_pdf_pages()
    """
    with open(json_path, "r", encoding="utf-8") as f:
        pages = json.load(f)

    # Basic validation
    for page in pages:
        if "page_number" not in page or "text" not in page:
            raise ValueError("Invalid pages JSON format")

        if not isinstance(page["page_number"], int):
            raise TypeError("page_number must be int")

        if not isinstance(page["text"], str):
            raise TypeError("text must be str")

    return pages

import json
from typing import List, Dict


def save_chapters_with_sections_to_json(
    chapters: List[Dict],
    output_path: str,
    pretty: bool = True
) -> None:
    """
    Save chapters with their sections to a JSON file.

    Expected structure:
    [
      {
        "chapter_number": int,
        "chapter_name": str,
        "sections": [
          {
            "section_number": str,
            "section_name": str,
            "text": str
          }
        ]
      }
    ]
    """
    with open(output_path, "w", encoding="utf-8") as f:
        if pretty:
            json.dump(chapters, f, indent=2, ensure_ascii=False)
        else:
            json.dump(chapters, f, ensure_ascii=False)


def load_chapters_with_sections_from_json(
    json_path: str
) -> List[Dict]:
    """
    Load chapters with sections from a JSON file.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        chapters = json.load(f)

    # Basic validation (lightweight, on purpose)
    for ch in chapters:
        if "chapter_number" not in ch or "sections" not in ch:
            raise ValueError("Invalid chapter JSON format")

        for sec in ch["sections"]:
            if "section_number" not in sec or "text" not in sec:
                raise ValueError("Invalid section JSON format")

    return chapters

def save_validation_report(
    report: Dict[str, Any],
    output_path: str,
    indent: int = 2
) -> None:
    """
    Save validator report (summary, errors, warnings) to a JSON file.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=indent)