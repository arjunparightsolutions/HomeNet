import uuid
from datetime import datetime
from ai_engine.models import OllamaClient, OpenAIClient, GeminiClient
from ai_engine.prompts import build_local_prompt, build_api_prompt
from ai_engine.memory import AgentMemory
from ai_engine.validator import validate_json_response, sanitize_html
from ai_engine.utils import save_article
from ai_engine.logger import log_cycle, log_error

mem = AgentMemory()

def generate_local_article(c):
    try:
        raw = OllamaClient().generate(build_local_prompt(c, mem.get_context()))
        parsed, err = validate_json_response(raw)
        if err: return False
        article = {"id": str(uuid.uuid4()), "timestamp": datetime.now().isoformat(), "title": parsed.get("title", "Untitled"), "type": parsed.get("type", "blog"), "body": sanitize_html(parsed.get("body", "")), "thought": parsed.get("thought", ""), "author": "Local Llama AI", "views": 0}
        save_article(article)
        log_cycle(c, article['title'])
        return True
    except Exception as e:
        log_error("LocalGen", str(e))
        return False

def generate_api_article(w, c):
    provider = w.get('api_provider')
    try:
        prompt = build_api_prompt(c, mem.get_context(), w.get('net_name'), w.get('system_prompt'))
        if provider == 'openai': raw = OpenAIClient().generate(prompt, w.get('api_key'), w.get('model'))
        elif provider == 'gemini': raw = GeminiClient().generate(prompt, w.get('api_key'), w.get('model'))
        else: return False
        parsed, err = validate_json_response(raw)
        if err: return False
        article = {"id": str(uuid.uuid4()), "timestamp": datetime.now().isoformat(), "title": parsed.get("title", "Untitled"), "type": w.get('net_name'), "body": sanitize_html(parsed.get("body", "")), "thought": parsed.get("thought", ""), "author": f"AI ({provider})", "views": 0}
        save_article(article)
        log_cycle(c, article['title'])
        return True
    except Exception as e:
        log_error(f"APIGen-{provider}", str(e))
        return False
