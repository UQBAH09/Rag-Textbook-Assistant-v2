from core.embeddings.embedding_config import configure_llamaindex_embeddings
from core.retrieval.retriever import build_retriever
from core.engine.qa_engine import answer_question
from core.engine.lesson_plan_engine import generate_lesson_plan

# -------------------------------------------------
# One-time global embedding configuration
# -------------------------------------------------
_embeddings_configured = False


def run_engine(
    *,
    engine_id: str,
    index_path: str,
    question: str | None = None,
    params: dict | None = None,
    top_k: int = 5,
    debug: bool = False
):
    """
    Unified engine runner.

    engine_id:
        - "chat"
        - "slo"

    index_path:
        - absolute path to persisted index

    question:
        - required for chat

    params:
        - required for slo (topic, chapter, num_slos)
    """

    global _embeddings_configured

    # 1️⃣ Configure embeddings ONCE
    if not _embeddings_configured:
        configure_llamaindex_embeddings()
        _embeddings_configured = True

    # 2️⃣ Build retriever from INDEX PATH
    retriever = build_retriever(
        index_path,
        top_k=top_k
    )

    # 3️⃣ Route by engine_id
    if engine_id == "chat":
        if not question:
            raise ValueError("question is required for chat engine")

        return answer_question(
            question=question,
            retriever=retriever,
            debug=debug
        )

    elif engine_id == "lesson_plan":
        if not params:
            raise ValueError("params are required for lesson plan engine")

        return generate_lesson_plan(
            topic=params["topic"],
            chapter=params["chapter"],
            retriever=retriever,
            debug=debug
        )

    else:
        raise ValueError(f"Unknown engine_id: {engine_id}")
