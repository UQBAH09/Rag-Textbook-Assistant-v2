from core.retrieval.retriever import retrieve
from core.assembly.context_builder import build_context
from core.prompting.lesson_plan_prompt import build_lesson_plan_prompt
from core.llm.ollama_client import generate_text


def generate_lesson_plan(
    topic: str,
    chapter: str,
    retriever,
    debug: bool = False
) -> str:
    """
    Generate a lesson plan using RAG.
    """

    query = f"{topic} in {chapter}"
    results = retrieve(query, retriever, debug_mode=debug)

    assembled = build_context(results)
    context_text = assembled["context"]

    if not context_text.strip():
        return "No relevant content found for the selected topic."

    prompt = build_lesson_plan_prompt(
        topic=topic,
        chapter=chapter,
        context=context_text
    )

    if debug:
        print("\n===== LESSON PLAN PROMPT =====\n")
        print(prompt)

    return generate_text(prompt)
