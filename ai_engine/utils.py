import json, os
from datetime import datetime
from ai_engine.config import CONTENT_FILE, WEBSITES_FILE

def get_articles():
    if not os.path.exists(CONTENT_FILE): return []
    try:
        with open(CONTENT_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    except: return []

def save_article(article):
    articles = get_articles()
    articles.append(article)
    with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=4, ensure_ascii=False)

def get_websites():
    if not os.path.exists(WEBSITES_FILE): return []
    try:
        with open(WEBSITES_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    except: return []

def get_recent_titles(limit=3):
    return [a.get('title') for a in get_articles()[-limit:]]
