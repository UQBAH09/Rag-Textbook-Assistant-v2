def build_qa_prompt(query: str, context: str) -> str:
    """
    Build a strict QA prompt that forces the LLM
    to answer only from the provided context.

    Args:
        query (str): User question
        context (str): Assembled textbook context

    Returns:
        str: Prompt to send to LLM
    """

    return f"""
You are an educational assistant.

You must answer the QUESTION using ONLY the TEXTBOOK CONTENT provided below.

Rules you must follow:
- Do NOT use any external knowledge.
- Do NOT make assumptions.
- If the answer is not explicitly stated or clearly implied in the content,
  respond with exactly:
  "Not found in the provided text."

TEXTBOOK CONTENT:
{context}

QUESTION:
{query}

ANSWER:
""".strip()
