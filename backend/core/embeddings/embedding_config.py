"""
Embedding configuration for Stage 2 (Vectorization).

This module configures LlamaIndex to use Ollama
for generating text embeddings.

IMPORTANT:
- This file must NOT be executed directly.
- It is imported and called from a runner script.
"""

from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings


def configure_llamaindex_embeddings(
    model_name: str = "nomic-embed-text",
    base_url: str = "http://localhost:11434",
):
    """
    Configure LlamaIndex to use Ollama embeddings.

    Args:
        model_name (str): Ollama embedding model name
        base_url (str): Ollama server URL
    """

    # Set embedding model (this is what creates vectors)
    Settings.embed_model = OllamaEmbedding(
        model_name=model_name,
        base_url=base_url,
    )

    # Disable LLM usage for Stage 2 (embedding only)
    Settings.llm = None
