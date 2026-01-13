from typing import List, Dict, Any

# ===============================
# Required schema for a chunk
# ===============================
REQUIRED_FIELDS = {
    "chunk_id",
    "book_id",
    "chapter_number",
    "chapter_name",
    "section_number",
    "section_name",
    "chapter_page_start",
    "chapter_page_end",
    "text"
}


def validate_chunks(chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate chunk integrity, structure, and metadata correctness.

    This validator is READ-ONLY:
    - It never modifies chunks
    - It only reports errors and warnings
    """

    errors = []
    warnings = []

    # Track section consistency
    section_name_map = {}
    seen_sections = set()
    active_section = None

    # Track ordering sanity
    last_chapter = None
    last_section = None

    for idx, chunk in enumerate(chunks):
        chunk_id = chunk.get("chunk_id", f"<missing-id-{idx}>")

        # ==================================================
        # CHECK 1: Required fields
        # ==================================================
        missing = REQUIRED_FIELDS - chunk.keys()
        if missing:
            errors.append({
                "chunk_id": chunk_id,
                "type": "MISSING_FIELDS",
                "message": f"Missing fields: {sorted(missing)}"
            })
            continue

        # ==================================================
        # CHECK 2: Text validity
        # ==================================================
        text = chunk["text"]
        if not isinstance(text, str) or not text.strip():
            errors.append({
                "chunk_id": chunk_id,
                "type": "INVALID_TEXT",
                "message": "Text is empty or not a string"
            })
            continue

        text_len = len(text.strip())

        # ==================================================
        # CHECK 3: Chunk size sanity (warnings only)
        # ==================================================
        if text_len < 90:
            warnings.append({
                "chunk_id": chunk_id,
                "type": "SMALL_CHUNK",
                "message": f"Chunk too small ({text_len} chars)"
            })

        if text_len > 1200:
            warnings.append({
                "chunk_id": chunk_id,
                "type": "LARGE_CHUNK",
                "message": f"Chunk too large ({text_len} chars)"
            })

        # ==================================================
        # CHECK 4: Chapter-level page validity
        # ==================================================
        cps = chunk["chapter_page_start"]
        cpe = chunk["chapter_page_end"]

        if not isinstance(cps, int) or not isinstance(cpe, int):
            errors.append({
                "chunk_id": chunk_id,
                "type": "INVALID_PAGE_TYPE",
                "message": "Chapter page numbers must be integers"
            })
            continue

        if cps <= 0 or cpe <= 0:
            errors.append({
                "chunk_id": chunk_id,
                "type": "INVALID_PAGE_RANGE",
                "message": "Chapter page numbers must be positive"
            })
            continue

        if cps > cpe:
            errors.append({
                "chunk_id": chunk_id,
                "type": "PAGE_ORDER_ERROR",
                "message": (
                    f"chapter_page_start ({cps}) > "
                    f"chapter_page_end ({cpe})"
                )
            })
            continue

        # ==================================================
        # CHECK 5: Section consistency & contiguity
        # ==================================================
        section_key = (chunk["chapter_number"], chunk["section_number"])
        section_name = chunk["section_name"]

        # Section name must be stable
        if section_key in section_name_map:
            if section_name_map[section_key] != section_name:
                errors.append({
                    "chunk_id": chunk_id,
                    "type": "SECTION_NAME_MISMATCH",
                    "message": (
                        f"Section {section_key} has inconsistent names: "
                        f"'{section_name_map[section_key]}' vs '{section_name}'"
                    )
                })
                continue
        else:
            section_name_map[section_key] = section_name

        # Section should not reappear after closing
        if active_section is None:
            active_section = section_key
        elif section_key != active_section:
            if section_key in seen_sections:
                warnings.append({
                    "chunk_id": chunk_id,
                    "type": "SECTION_REOPENED",
                    "message": (
                        f"Section {section_key} reappeared after being closed"
                    )
                })
            seen_sections.add(active_section)
            active_section = section_key

        # ==================================================
        # CHECK 6: Chapter & section ordering sanity (soft)
        # ==================================================
        chapter = chunk["chapter_number"]
        section = chunk["section_number"]

        if last_chapter is not None and chapter < last_chapter:
            warnings.append({
                "chunk_id": chunk_id,
                "type": "CHAPTER_ORDER",
                "message": (
                    f"Chapter number decreased "
                    f"({chapter} < {last_chapter})"
                )
            })

        if last_section is not None and chapter == last_chapter:
            if section < last_section:
                warnings.append({
                    "chunk_id": chunk_id,
                    "type": "SECTION_ORDER",
                    "message": (
                        f"Section order decreased "
                        f"({section} < {last_section})"
                    )
                })

        last_chapter = chapter
        last_section = section

    # ==================================================
    # FINAL REPORT
    # ==================================================
    return {
        "summary": {
            "total_chunks": len(chunks),
            "errors": len(errors),
            "warnings": len(warnings)
        },
        "errors": errors,
        "warnings": warnings
    }
