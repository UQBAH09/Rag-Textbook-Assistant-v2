from core.retrieval.retriever import retrieve
from core.assembly.context_builder import build_context
from core.prompting.qa_prompt import build_qa_prompt
from core.llm.ollama_client import generate_text


def answer_question(
    question: str,
    retriever,
    debug: bool = False
) -> str:
    """
    End-to-end QA over a textbook using RAG.

    Parameters
    ----------
    question : str
        User question
    retriever :
        Pre-built retriever (already bound to an index)
    """

    # 1️⃣ Retrieve relevant chunks
    results = retrieve(
        query=question,
        retriever=retriever,
        debug_mode=debug
    )

    # 2️⃣ Assemble context
    assembled = build_context(results)
    context_text = assembled["context"]

    if not context_text.strip():
        return "Not found in the provided text."

    # 3️⃣ Build prompt
    prompt = build_qa_prompt(question, context_text)

    if debug:
        print("\n===== PROMPT =====\n")
        print(prompt)

    # 4️⃣ Generate answer
    return generate_text(prompt)
