import json
def validate_json_response(raw):
    try:
        parsed = json.loads(raw)
        if 'title' not in parsed or 'body' not in parsed: return None, "Missing fields."
        return parsed, None
    except json.JSONDecodeError as e: return None, str(e)
def sanitize_html(body): return body.replace("<script", "&lt;script").replace("</script>", "&lt;/script&gt;")
