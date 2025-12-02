import requests

class LocalLLM:
    """Call local Ollama LLM."""
    def __init__(self, model="gemma3:1b", url="http://localhost:11434/api/chat"):
        self.model = model
        self.url = url

    def ask(self, prompt: str, system: str | None = None) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {"model": self.model, "messages": messages, "stream": False}
        try:
            res = requests.post(self.url, json=payload, timeout=300)  # increased timeout
            res.raise_for_status()
        except requests.RequestException as e:
            return f"ERROR: {e}"

        data = res.json()
        # Return content from response
        return data.get("message", {}).get("content", "")
