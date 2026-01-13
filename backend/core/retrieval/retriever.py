from llama_index.core.retrievers import VectorIndexRetriever
from core.index.index_retriever import load_index


def build_retriever(persist_dir: str, top_k: int = 5) -> VectorIndexRetriever:
    """Load index and return a VectorIndexRetriever."""
    index = load_index(persist_dir)
    return VectorIndexRetriever(index=index, similarity_top_k=top_k)


def retrieve(query: str, retriever: VectorIndexRetriever, debug_mode: bool = False):
    """
    Returns List[NodeWithScore]
    """
    results = retriever.retrieve(query)

    if debug_mode:
        from core.retrieval.debug import print_results
        print_results(results)

    return results
