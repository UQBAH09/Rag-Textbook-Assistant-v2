from typing import List, Dict
from llama_index.core.schema import NodeWithScore


def build_context(
    results: List[NodeWithScore],
    max_chars: int = 4000
) -> Dict:
    """
    Assemble retrieved nodes into a clean context block.

    Args:
        results (List[NodeWithScore]): Retrieved chunks
        max_chars (int): Max characters allowed in context

    Returns:
        Dict with:
            - context (str)
            - citations (List[Dict])
            - used_chunks (int)
    """

    # Sort by relevance score (descending)
    results = sorted(results, key=lambda r: r.score, reverse=True)

    context_parts = []
    citations = []
    seen_texts = set()
    current_length = 0

    for r in results:
        node = r.node
        text = node.get_content().strip()

        # Deduplicate identical chunks
        if text in seen_texts:
            continue
        seen_texts.add(text)

        meta = node.metadata or {}

        header = (
            f"[Chapter {meta.get('chapter_number')} "
            f"({meta.get('chapter_name')}), "
            f"Section {meta.get('section_number')} "
            f"({meta.get('section_name')}), "
            f"Pages {meta.get('page_start')}-{meta.get('page_end')}]"
        )

        block = f"{header}\n{text}\n"

        # Enforce max length
        if current_length + len(block) > max_chars:
            break

        context_parts.append(block)
        current_length += len(block)

        citations.append({
            "chapter": meta.get("chapter_number"),
            "section": meta.get("section_number"),
            "pages": f"{meta.get('page_start')}-{meta.get('page_end')}",
            "score": round(r.score, 4)
        })

    return {
        "context": "\n".join(context_parts),
        "citations": citations,
        "used_chunks": len(context_parts)
    }
