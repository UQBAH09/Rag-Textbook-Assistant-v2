import re
from typing import List, Dict, Optional


SECTION_HEADER_PATTERN = re.compile(r"^(\d+)\.(\d+)\b\s*(.*)")


def detect_section_candidates_in_chapter(chapter: Dict) -> List[Dict]:
    """
    Detect raw section candidates inside a single chapter.
    No ordering or cleanup rules applied here.
    """
    chapter_num = int(chapter["chapter_number"])
    lines = [l.strip() for l in chapter["text"].splitlines() if l.strip()]

    candidates: List[Dict] = []
    current: Optional[Dict] = None

    for line in lines:
        match = SECTION_HEADER_PATTERN.match(line)

        if match:
            sec_chapter = int(match.group(1))
            sec_index = int(match.group(2))
            sec_title = match.group(3).strip()

            # Must belong to this chapter
            if sec_chapter != chapter_num:
                if current:
                    current["text"] += line + " "
                continue

            if current:
                candidates.append(current)

            current = {
                "section_number": f"{sec_chapter}.{sec_index}",
                "section_name": sec_title,
                "text": ""
            }
            continue

        if current:
            current["text"] += line + " "

    if current:
        candidates.append(current)

    return candidates


def remove_empty_sections(sections: List[Dict], min_chars: int = 30) -> List[Dict]:
    """
    Remove sections with insufficient text (TOC, summaries, noise).
    """
    cleaned = []

    for sec in sections:
        body = (sec.get("text") or "").strip()
        if len(body) < min_chars:
            continue

        sec["text"] = body
        cleaned.append(sec)

    return cleaned


def keep_sections_starting_from_one(
    sections: List[Dict],
    chapter_number: int
) -> List[Dict]:
    """
    Drop everything before X.1.
    """
    target = f"{chapter_number}.1"

    for i, sec in enumerate(sections):
        if sec["section_number"] == target:
            return sections[i:]

    return []


def merge_duplicate_sections(sections: List[Dict]) -> List[Dict]:
    """
    Merge duplicate section numbers (e.g., multiple 1.1).
    """
    merged = {}
    order = []

    for sec in sections:
        sec_num = sec["section_number"]

        if sec_num not in merged:
            merged[sec_num] = {
                "section_number": sec_num,
                "section_name": sec.get("section_name", ""),
                "text": sec.get("text", "").strip()
            }
            order.append(sec_num)
        else:
            merged[sec_num]["text"] += " " + sec.get("text", "").strip()
            if not merged[sec_num]["section_name"]:
                merged[sec_num]["section_name"] = sec.get("section_name", "")

    # Normalize titles
    for sec in merged.values():
        sec["section_name"] = " ".join(sec["section_name"].split())

    return [merged[num] for num in order]


def _section_sort_key(sec: Dict) -> int:
    return int(sec["section_number"].split(".")[1])


def detect_sections(chapters: List[Dict], min_chars: int = 30) -> List[Dict]:
    """
    FINAL section detection pipeline.
    """
    out = []

    for ch in chapters:
        raw_sections = detect_section_candidates_in_chapter(ch)

        cleaned_sections = remove_empty_sections(
            raw_sections,
            min_chars=min_chars
        )

        cleaned_sections = keep_sections_starting_from_one(
            cleaned_sections,
            chapter_number=ch["chapter_number"]
        )

        cleaned_sections = merge_duplicate_sections(cleaned_sections)

        # Ensure correct order (X.1 → X.2 → X.3)
        cleaned_sections = sorted(
            cleaned_sections,
            key=_section_sort_key
        )

        out.append({
            "chapter_number": ch["chapter_number"],
            "chapter_name": ch.get("chapter_name", ""),
            "page_start": ch["page_start"],
            "page_end": ch["page_end"],
            "sections": cleaned_sections
        })

    return out
