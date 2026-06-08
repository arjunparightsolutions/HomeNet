from ai_engine.models import OllamaClient
from ai_engine.logger import log_error
import json
def generate_search_summary(query, context):
    try:
        prompt = f"AI Search Summarizer.\nQuery: {query}\nContext:\n{context}\nProvide summary in JSON: {{'summary': '...'}}"
        raw = OllamaClient().generate(prompt)
        return json.loads(raw).get('summary', 'Could not generate summary.')
    except Exception as e:
        log_error("Summarizer", str(e))
        return "Summarizer offline."
