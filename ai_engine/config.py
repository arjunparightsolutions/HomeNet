import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONTENT_FILE = os.path.join(BASE_DIR, 'content', 'articles.json')
WEBSITES_FILE = os.path.join(BASE_DIR, 'content', 'websites.json')
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
GEMINI_API_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
DEFAULT_OLLAMA_MODEL = "llama3.2:1b"
DEFAULT_OPENAI_MODEL = "gpt-4o"
DEFAULT_GEMINI_MODEL = "gemini-1.5-flash"
