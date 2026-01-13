import re
from typing import List, Dict

SENTENCE_SPLIT_REGEX = re.compile(r'(?<=[.!?])\s+')


def split_into_sentences(text: str) -> List[str]:
    text = text.strip()
    if not text:
        return []
    sentences = SENTENCE_SPLIT_REGEX.split(text)
    return [s.strip() for s in sentences if s.strip()]


def chunk_text(
    text: str,
    min_chars: int = 300,
    max_chars: int = 1000
) -> List[str]:
    sentences = split_into_sentences(text)
    chunks = []

    current_chunk = []
    current_len = 0

    for sentence in sentences:
        sentence = sentence.strip()
        sentence_len = len(sentence)
        

        # Force split very long sentences
        if sentence_len > max_chars:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk, current_len = [], 0

            for i in range(0, sentence_len, max_chars):
                chunks.append(sentence[i:i + max_chars])
            continue

        if current_len + sentence_len <= max_chars:
            current_chunk.append(sentence)
            current_len += sentence_len + 1  # +1 for space
        else:
            if current_len >= min_chars:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]
                current_len = sentence_len
            else:
                current_chunk.append(sentence)
                current_len += sentence_len + 1

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def chunk_sections(
    parsed_chapters: List[Dict],
    book_id: str,
    min_chars: int = 300,
    max_chars: int = 800
) -> List[Dict]:
    all_chunks = []

    for chapter in parsed_chapters:
        chapter_number = chapter["chapter_number"]
        chapter_name = chapter["chapter_name"]

        for section in chapter["sections"]:
            chunks = chunk_text(
                section["text"],
                min_chars=min_chars,
                max_chars=max_chars
            )

            for idx, chunk in enumerate(chunks, start=1):
                chunk_id = f"{book_id}_{chapter_number}_{section['section_number']}_{idx:03d}"

                all_chunks.append({
                    "chunk_id": chunk_id,
                    "book_id": book_id,
                    "chapter_number": chapter_number,
                    "chapter_name": chapter_name,
                    "section_number": section["section_number"],
                    "section_name": section["section_name"],
                    "chapter_page_start": chapter["page_start"],
                    "chapter_page_end": chapter["page_end"],
                    "length_of_text": len(chunk.strip()),
                    "text": chunk.strip()
                })

    return all_chunks
