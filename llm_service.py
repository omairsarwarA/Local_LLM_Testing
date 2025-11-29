import requests

class LocalLLM:
    def __init__(self, model="gemma3:1b", url="http://localhost:11434/api/chat"):
        self.model = model
        self.url = url

    def ask(self, prompt):
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
        response = requests.post(self.url, json=payload)
        # print(response.text)
        return response.json().get("message", "").get("content", "")
