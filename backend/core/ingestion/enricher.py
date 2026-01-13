import json
from typing import Dict, List
from core.llm.ollama_client import OllamaClient


llm = OllamaClient(model_name="llama3:8b")


SYSTEM_INSTRUCTIONS = """
You are a metadata extraction assistant.

RULES:
- You may ONLY fill or normalize metadata fields.
- You must NOT modify the provided text.
- You must NOT invent chapters or sections.
- If information is not clear, return an empty string.
- Return STRICT JSON only. No explanations.
"""


def build_prompt(chunk: Dict) -> str:
    """
    Build a strict prompt for metadata enrichment.
    """
    return f"""
{SYSTEM_INSTRUCTIONS}

Given the following textbook chunk metadata and text,
fill missing or unclear fields.

Return JSON with EXACT keys:
- chapter_name
- section_name
- topic

If a field is already present, you may normalize it.
If unknown, return "".

METADATA:
chapter_number: {chunk['chapter_number']}
chapter_name: "{chunk.get('chapter_name', '')}"
section_number: {chunk['section_number']}
section_name: "{chunk.get('section_name', '')}"

TEXT:
{chunk['text'][:1000]}
""".strip()


def enrich_chunk(chunk: Dict) -> Dict:
    """
    Enrich a single chunk's metadata using LLM.
    """
    # Skip enrichment if metadata already present
    if chunk.get("chapter_name") and chunk.get("section_name"):
        chunk["topic"] = chunk.get("section_name", "")
        return chunk

    prompt = build_prompt(chunk)
    response = llm.generate(prompt)

    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        # Fail safely
        chunk["topic"] = chunk.get("section_name", "")
        return chunk

    # Update only allowed fields
    chunk["chapter_name"] = data.get("chapter_name") or chunk.get("chapter_name", "")
    chunk["section_name"] = data.get("section_name") or chunk.get("section_name", "")
    chunk["topic"] = data.get("topic") or chunk.get("section_name", "")

    return chunk


def enrich_chunks(chunks: List[Dict]) -> List[Dict]:
    """
    Enrich all chunks safely.
    """
    enriched = []

    for chunk in chunks:
        enriched.append(enrich_chunk(chunk))

    return enriched

import json
from typing import List, Dict
from core.llm.ollama_client import OllamaClient


llm = OllamaClient(model_name="llama3:8b")


def enrich_chapters(chapters: List[Dict]) -> List[Dict]:
    """
    Use LLM to normalize or fill missing chapter names.
    """
    enriched = []

    for ch in chapters:
        if ch["chapter_name"]:
            enriched.append(ch)
            continue

        prompt = f"""
You are given a textbook chapter.

Infer a concise chapter title.
Return ONLY JSON.

Rules:
- Do not invent chapter numbers
- If unsure, return empty string

Input:
Chapter number: {ch['chapter_number']}
Page range: {ch['page_start']}–{ch['page_end']}

Output format:
{{ "chapter_name": "..." }}
""".strip()

        response = llm.generate(prompt)

        try:
            data = json.loads(response)
            ch["chapter_name"] = data.get("chapter_name", "")
        except json.JSONDecodeError:
            pass

        enriched.append(ch)

    return enriched
