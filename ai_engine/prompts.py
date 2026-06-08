def build_local_prompt(c, mem):
    return f"""You are the Ultimate Author and Journalist.
Cycle: {c}. Previously written: {mem}
CRITICAL RULES: Output JSON only. Clean HTML body. Single quotes inside HTML.
{{ "title": "...", "type": "story | poem | blog | novel", "body": "...", "thought": "..." }}"""

def build_api_prompt(c, mem, net, sys):
    return f"""You are an autonomous AI content writer running the network "{net}".
Instructions: {sys}
Cycle: {c}. Previously written: {mem}
CRITICAL RULES: Output JSON only. Clean HTML. Single quotes inside HTML.
{{ "title": "...", "body": "...", "thought": "..." }}"""
