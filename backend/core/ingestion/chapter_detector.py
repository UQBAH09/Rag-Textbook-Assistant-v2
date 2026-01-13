import re
from typing import List, Dict


CHAPTER_PATTERN = re.compile(r"^CHAPTER\s+(\d+)\b\s*(.*)", re.IGNORECASE)
CHAPTER_TITLE_SAME_LINE = re.compile(r"^CHAPTER\s+\d+\b\s+(.*)$", re.IGNORECASE)
CHAPTER_TITLE_NEXT_LINE = re.compile(r"^CHAPTER\s+\d+\b\s*$", re.IGNORECASE)

FORBIDDEN_TITLE_WORDS = ["CHAPTER", "CONTENT", "CONTENTS", "TABLE OF CONTENTS"]


def detect_chapter_candidates(pages: List[Dict]) -> List[Dict]:
    candidates = []

    for page in pages:
        page_num = page["page_number"]
        lines = page["text"].splitlines()

        # Slightly deeper scan for safety
        for line in lines[:10]:
            line = line.strip()
            match = CHAPTER_PATTERN.match(line)
            if match:
                candidates.append({
                    "chapter_number": int(match.group(1)),
                    "chapter_name": match.group(2).strip(),
                    "page_number": page_num
                })

    return candidates


def filter_real_chapters(
    candidates: List[Dict],
    min_page_gap: int = 5
) -> List[Dict]:
    real_chapters = []
    seen_numbers = set()

    last_page = -999
    last_chapter_num = 0

    for c in candidates:
        ch_num = c["chapter_number"]
        page = c["page_number"]

        if ch_num <= last_chapter_num:
            continue

        if page - last_page < min_page_gap:
            continue

        if ch_num in seen_numbers:
            continue

        real_chapters.append(c)
        seen_numbers.add(ch_num)
        last_page = page
        last_chapter_num = ch_num

    return real_chapters


def extract_chapter_name_from_text(text: str, max_lines: int = 3) -> str:
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    for i, line in enumerate(lines):
        m = CHAPTER_TITLE_SAME_LINE.match(line)
        if m:
            title = m.group(1).strip()
            title = _strip_forbidden_suffix(title)
            return title

        if CHAPTER_TITLE_NEXT_LINE.match(line):
            title_parts = []

            for j in range(1, max_lines + 1):
                if i + j >= len(lines):
                    break

                candidate = lines[i + j]

                if re.match(r"^\d+(\.\d+)*", candidate):
                    break

                if _contains_forbidden_words(candidate):
                    break

                if len(candidate.split()) > 6:
                    break

                if any(p in candidate for p in ".;,"):
                    break

                title_parts.append(candidate)

            return " ".join(title_parts).strip()

    return ""


def _contains_forbidden_words(text: str) -> bool:
    upper = text.upper()
    return any(word in upper for word in FORBIDDEN_TITLE_WORDS)


def _strip_forbidden_suffix(text: str) -> str:
    upper = text.upper()
    for word in FORBIDDEN_TITLE_WORDS:
        idx = upper.find(word)
        if idx > 0:
            return text[:idx].strip()
    return text


def extract_chapter_text(
    pages: List[Dict],
    page_start: int,
    page_end: int
) -> str:
    parts = []

    for page in pages:
        if page_start <= page["page_number"] <= page_end:
            parts.append(page["text"])

    return "\n".join(parts).strip()


def build_chapters(
    pages: List[Dict],
    real_chapters: List[Dict]
) -> List[Dict]:
    chapters = []
    last_page_num = pages[-1]["page_number"]

    for idx, ch in enumerate(real_chapters):
        start_page = ch["page_number"]
        end_page = (
            real_chapters[idx + 1]["page_number"] - 1
            if idx + 1 < len(real_chapters)
            else last_page_num
        )

        chapter_text = extract_chapter_text(pages, start_page, end_page)

        chapter_name = ch["chapter_name"]
        if not chapter_name:
            chapter_name = extract_chapter_name_from_text(chapter_text)

        chapter_name = " ".join(chapter_name.split())

        chapters.append({
            "chapter_number": ch["chapter_number"],
            "chapter_name": chapter_name,
            "page_start": start_page,
            "page_end": end_page,
            "text": chapter_text
        })

    return chapters


def detect_chapters(pages: List[Dict]) -> List[Dict]:
    candidates = detect_chapter_candidates(pages)
    real = filter_real_chapters(candidates)
    return build_chapters(pages, real)
