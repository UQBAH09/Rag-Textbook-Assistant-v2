from typing import List, Dict
from core.ingestion.chapter_detector import detect_chapters
from core.ingestion.section_detector import detect_sections

def parse_structure(pages: List[Dict]) -> List[Dict]:
    """
    Parse pages into chapters and sections.

    Args:
        pages (List[Dict]): Output from load_pdf_pages()

    Returns:
        List[Dict]: Chapters with detected sections
    """
    chapters_without_sections = detect_chapters(pages)
    chapters_with_sections = detect_sections(chapters_without_sections)

    return chapters_with_sections