from pathlib import Path

# =========================
# PROJECT ROOT
# =========================
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

# =========================
# TOP-LEVEL DIRS
# =========================
UPLOADS_DIR = PROJECT_ROOT / "uploads"
DATA_DIR = PROJECT_ROOT / "data"
INDEX_ROOT = DATA_DIR / "index"

# =========================
# BOOK-SPECIFIC PATHS
# =========================
def book_pdf_path(book_id: str) -> Path:
    return UPLOADS_DIR / f"{book_id}.pdf"


def book_data_dir(book_id: str) -> Path:
    return DATA_DIR / book_id


def book_index_dir(book_id: str) -> Path:
    return INDEX_ROOT / book_id
