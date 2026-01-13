from typing import Dict,List
import pdfplumber

def load_pdf_pages(pdf_path: str) -> List[Dict[str, str|int]]:
    # Load a PDF and extract text page by page.

    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for idx,page in enumerate(pdf.pages):
            text = page.extract_text().strip()

            if not text:
                continue
            
            pages.append({
                "page_number": idx + 1,
                "text": text
            })
    return pages