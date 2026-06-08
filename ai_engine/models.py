import requests
from ai_engine.config import *

class OllamaClient:
    def generate(self, prompt):
        payload = {"model": DEFAULT_OLLAMA_MODEL, "prompt": prompt, "stream": False, "format": "json"}
        res = requests.post(OLLAMA_API_URL, json=payload)
        res.raise_for_status()
        return res.json().get('response', '')

class OpenAIClient:
    def generate(self, prompt, key, model):
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        payload = {"model": model or DEFAULT_OPENAI_MODEL, "messages": [{"role": "system", "content": "JSON content generator."}, {"role": "user", "content": prompt}], "response_format": {"type": "json_object"}}
        res = requests.post(OPENAI_API_URL, headers=headers, json=payload)
        res.raise_for_status()
        return res.json()['choices'][0]['message']['content']

class GeminiClient:
    def generate(self, prompt, key, model):
        url = GEMINI_API_URL_TEMPLATE.format(model=model or DEFAULT_GEMINI_MODEL, api_key=key)
        payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"response_mime_type": "application/json"}}
        res = requests.post(url, headers={"Content-Type": "application/json"}, json=payload)
        res.raise_for_status()
        return res.json()['candidates'][0]['content']['parts'][0]['text']
