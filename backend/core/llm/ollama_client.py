import ollama


class OllamaClient:
    """
    LLM client wrapper for Ollama.
    """

    def __init__(self, model_name: str = "llama3:8b"):
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        response = ollama.chat(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"].strip()


_default_client = OllamaClient()

def generate_text(prompt: str) -> str:
    return _default_client.generate(prompt)
