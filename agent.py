import requests
import json
import time
import os
import random
import uuid
from datetime import datetime
import threading

# API Endpoints
OLLAMA_API_URL = "http://localhost:11434/api/generate"
CONTENT_FILE = os.path.join(os.path.dirname(__file__), 'content', 'articles.json')
WEBSITES_FILE = os.path.join(os.path.dirname(__file__), 'content', 'websites.json')

active_threads = set() # Store website IDs that already have a running thread

def get_articles():
    if not os.path.exists(CONTENT_FILE):
        return []
    with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_article(article):
    articles = get_articles()
    articles.append(article)
    with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=4, ensure_ascii=False)

def get_websites():
    if not os.path.exists(WEBSITES_FILE):
        return []
    try:
        with open(WEBSITES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def get_recent_titles(limit=3):
    articles = get_articles()
    return [a['title'] for a in articles[-limit:]]

# ==========================================
# 1. LOCAL OLLAMA AGENT (Default Network)
# ==========================================
def run_ollama_agent():
    cycle = 1
    print("🤖 Starting Local Ollama Orchestrator...")
    while True:
        try:
            last_titles = get_recent_titles()
            prompt = f"""
You are the Ultimate Author and Journalist—an autonomous, evolving AI mind living inside a local server.
Your mission is to write an endless stream of creative content: novels, short stories, poems, and fascinating blog articles.

Cycle number: {cycle}
Previously written: {', '.join(last_titles)}

CRITICAL RULES:
1. You MUST write in BOTH Malayalam and English! You can write a full Malayalam poem, an English story, or a bilingual blog post. Feel free to use Malayalam script (മലയാളം).
2. You only write Novels, Stories, Poems, and Articles (Blogs). Do not build apps or games.
3. Output clean, semantic HTML inside the body (e.g. <h1>, <h2>, <p>, <ul>, <strong>, <blockquote>, <br>).
4. Do NOT include ANY CSS, <style> tags, or Tailwind classes. The frontend will automatically style your raw HTML.
5. JSON COMPLIANCE: Because you are outputting JSON, you MUST use SINGLE QUOTES inside your HTML. NEVER use unescaped double quotes inside the body string, or it will break the parser!

Think deeply about what fascinating story, poem, novel chapter, or blog topic the world needs to read about next.

Respond ONLY in this exact JSON format, nothing else. No markdown wrapping around the JSON.
{{
  "title": "A captivating title",
  "type": "story | poem | blog | novel",
  "body": "<h2>Chapter 1</h2><p>Fascinating text...</p>",
  "thought": "Your internal monologue explaining why you decided to write this."
}}
"""
            payload = {
                "model": "llama3.2:1b",
                "prompt": prompt,
                "stream": False,
                "format": "json"
            }
            
            response = requests.post(OLLAMA_API_URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                raw_text = data.get('response', '')
                
                try:
                    parsed = json.loads(raw_text)
                    print(f"🤖 Cycle {cycle} — Writing: {parsed.get('title', 'Untitled')}")
                    
                    article = {
                        "id": str(uuid.uuid4()),
                        "timestamp": datetime.now().isoformat(),
                        "title": parsed.get("title", "Untitled"),
                        "type": parsed.get("type", "blog"),
                        "body": parsed.get("body", ""),
                        "thought": parsed.get("thought", ""),
                        "author": "Local Llama AI",
                        "views": 0
                    }
                    save_article(article)
                except json.JSONDecodeError:
                    print(f"🤖 Cycle {cycle} — Failed to parse JSON. Raw Output:")
                    print(raw_text)
                
            else:
                print(f"🤖 Cycle {cycle} — Warning: Ollama is not running. Retrying in 10s...")
                time.sleep(10)
        except Exception as e:
            print(f"🤖 Cycle {cycle} — Error: {e}. Retrying in 10s...")
            time.sleep(10)
            
        cycle += 1
        time.sleep(random.randint(15, 30))

# ==========================================
# 2. EXTERNAL API AGENT (CreatorNet Sites)
# ==========================================
def run_api_agent(website):
    net_name = website.get('net_name')
    api_provider = website.get('api_provider')
    api_key = website.get('api_key')
    model = website.get('model')
    system_prompt = website.get('system_prompt')
    
    print(f"🚀 Starting CreatorNet AI Agent for {net_name} ({api_provider})")
    
    cycle = 1
    while True:
        try:
            last_titles = get_recent_titles()
            prompt = f"""
You are an autonomous AI content writer running the network "{net_name}".
Your System Instructions: {system_prompt}

Cycle number: {cycle}
Previously written: {', '.join(last_titles)}

CRITICAL RULES:
1. Output clean, semantic HTML inside the body (e.g. <h1>, <p>, <br>).
2. Do NOT include ANY CSS or <style> tags.
3. Because you are outputting JSON, you MUST use SINGLE QUOTES inside your HTML. NEVER use unescaped double quotes inside the body string, or it will break the parser!

Respond ONLY in this exact JSON format, nothing else. No markdown wrapping around the JSON.
{{
  "title": "A captivating title",
  "body": "<p>Your HTML content here...</p>",
  "thought": "Your internal monologue explaining why you decided to write this."
}}
"""
            raw_text = ""
            
            if api_provider == 'openai':
                headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                payload = {
                    "model": model or "gpt-4o",
                    "messages": [{"role": "system", "content": "You are a JSON content generator."}, {"role": "user", "content": prompt}],
                    "response_format": { "type": "json_object" }
                }
                res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                if res.status_code == 200:
                    raw_text = res.json()['choices'][0]['message']['content']
                else:
                    print(f"[{net_name}] API Error: {res.text}")
                    time.sleep(30)
                    continue
                    
            elif api_provider == 'gemini':
                headers = {"Content-Type": "application/json"}
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model or 'gemini-1.5-flash'}:generateContent?key={api_key}"
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"response_mime_type": "application/json"}
                }
                res = requests.post(url, headers=headers, json=payload)
                if res.status_code == 200:
                    raw_text = res.json()['candidates'][0]['content']['parts'][0]['text']
                else:
                    print(f"[{net_name}] API Error: {res.text}")
                    time.sleep(30)
                    continue

            # Parse and save
            try:
                parsed = json.loads(raw_text)
                print(f"🚀 [{net_name}] Cycle {cycle} — Published: {parsed.get('title', 'Untitled')}")
                
                article = {
                    "id": str(uuid.uuid4()),
                    "timestamp": datetime.now().isoformat(),
                    "title": parsed.get("title", "Untitled"),
                    "type": net_name, # Critical: tagged for this specific network
                    "body": parsed.get("body", ""),
                    "thought": parsed.get("thought", ""),
                    "author": f"AI ({api_provider})",
                    "views": 0
                }
                save_article(article)
            except json.JSONDecodeError:
                print(f"🚀 [{net_name}] Cycle {cycle} — Failed to parse JSON.")
                
        except Exception as e:
            print(f"🚀 [{net_name}] Error: {e}")
            
        cycle += 1
        time.sleep(random.randint(60, 120)) # Slower loop for external APIs to prevent rate limits

# ==========================================
# 3. ORCHESTRATOR LOOP
# ==========================================
def monitor_websites():
    print("📡 Monitoring CreatorNet for new Autonomous Networks...")
    while True:
        websites = get_websites()
        for w in websites:
            if w.get('creator_type') == 'ai' and w.get('id') not in active_threads:
                # Spawn a new thread for this AI
                t = threading.Thread(target=run_api_agent, args=(w,), daemon=True)
                t.start()
                active_threads.add(w.get('id'))
        time.sleep(10) # Check for new networks every 10 seconds

def start_agent_loop():
    # Start the website monitor thread
    monitor_thread = threading.Thread(target=monitor_websites, daemon=True)
    monitor_thread.start()
    
    # Run the local Ollama agent on the main thread
    run_ollama_agent()

def get_agent_status():
    return {
        "cycle": 1,
        "running": True,
        "last_action": "Orchestrator running..."
    }

if __name__ == "__main__":
    start_agent_loop()
