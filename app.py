import os
import json
import threading
import uuid
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from pyngrok import ngrok
from agent import start_agent_loop, get_agent_status
from nlp_utils import calculate_relevance

app = Flask(__name__)

CONTENT_FILE = os.path.join(os.path.dirname(__file__), 'content', 'articles.json')
WEBSITES_FILE = os.path.join(os.path.dirname(__file__), 'content', 'websites.json')
ANALYTICS_FILE = os.path.join(os.path.dirname(__file__), 'content', 'analytics.json')
HOSTED_DIR = os.path.join(os.path.dirname(__file__), 'content', 'hosted')
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), 'static', 'uploads') # In static so they can be served easily

def load_analytics():
    if not os.path.exists(ANALYTICS_FILE): return {}
    try:
        with open(ANALYTICS_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    except: return {}

def save_analytics(data):
    with open(ANALYTICS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def load_articles():
    if not os.path.exists(CONTENT_FILE):
        return []
    try:
        with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def save_article(article):
    articles = load_articles()
    articles.append(article)
    with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=4, ensure_ascii=False)

def load_websites():
    if not os.path.exists(WEBSITES_FILE):
        return []
    try:
        with open(WEBSITES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def save_website(website):
    websites = load_websites()
    websites.append(website)
    with open(WEBSITES_FILE, 'w', encoding='utf-8') as f:
        json.dump(websites, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/storynet')
def storynet():
    return render_template('storynet.html')

@app.route('/poemnet')
def poemnet():
    return render_template('poemnet.html')

@app.route('/blognet')
def blognet():
    return render_template('blognet.html')

@app.route('/novelnet')
def novelnet():
    return render_template('novelnet.html')

@app.route('/net/<path:net_name>')
def dynamic_net(net_name):
    # Track Analytics
    ip = request.remote_addr
    analytics = load_analytics()
    if net_name not in analytics:
        analytics[net_name] = {"visits": 0, "ips": []}
    analytics[net_name]["visits"] += 1
    if ip not in analytics[net_name]["ips"]:
        analytics[net_name]["ips"].append(ip)
    save_analytics(analytics)

    websites = load_websites()
    for w in websites:
        if w.get('net_name', '').lower() == net_name.lower():
            # Check if there is a lander file
            lander = w.get('lander_file')
            if lander:
                file_path = os.path.join(HOSTED_DIR, w.get('net_name'), lander)
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    # Inject Ads if enabled
                    if w.get('ads_enabled'):
                        ad_html = f"""
                        <div style="position:fixed; bottom:20px; right:20px; background:#fff; color:#000; padding:15px; border-radius:10px; box-shadow:0 10px 25px rgba(0,0,0,0.2); z-index:9999; max-width:250px;">
                            <div style="font-size:10px; text-transform:uppercase; color:#888; margin-bottom:5px;">Sponsored</div>
                            <img src="{w.get('ad_image', '')}" style="width:100%; border-radius:5px; margin-bottom:10px;">
                            <a href="{w.get('ad_link', '#')}" target="_blank" style="font-weight:bold; color:#000; text-decoration:none; display:block; margin-bottom:5px;">{w.get('ad_title', 'Ad')}</a>
                        </div>
                        """
                        if '</body>' in html_content:
                            html_content = html_content.replace('</body>', f'{ad_html}</body>')
                        else:
                            html_content += ad_html
                    return html_content
            
            # Fallback to dynamic template
            return render_template('dynamic_net.html', website=w)
    return "Network not found", 404

@app.route('/net/<path:net_name>/<path:filename>')
def serve_hosted_file(net_name, filename):
    file_path = os.path.join(HOSTED_DIR, net_name, filename)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "File not found", 404

@app.route('/debug')
def debug():
    return render_template('debug.html')

@app.route('/creatornet')
def creatornet():
    return render_template('creatornet.html')

@app.route('/api/websites')
def api_websites():
    return jsonify(load_websites())

@app.route('/api/search', methods=['GET'])
def api_search():
    query = request.args.get('q', '').strip()
    articles = load_articles()
    
    if not query:
        # Sort by views, then newest
        articles.sort(key=lambda x: (x.get('views', 0), x.get('timestamp', '')), reverse=True)
        return jsonify(articles)
        
    scored_articles = []
    for article in articles:
        score = calculate_relevance(article, query)
        if score > 0:
            article['_score'] = score
            scored_articles.append(article)
            
    # Sort by Relevance -> Views -> Date
    scored_articles.sort(key=lambda x: (x.get('_score', 0), x.get('views', 0), x.get('timestamp', '')), reverse=True)
    
    # Return top 50 results to optimize bandwidth
    return jsonify(scored_articles[:50])

@app.route('/api/register_net', methods=['POST'])
def api_register_net():
    data = request.json
    net_name = data.get('net_name')
    if not net_name:
        return jsonify({"error": "net_name required"}), 400
    
    website = {
        "id": str(uuid.uuid4()),
        "net_name": net_name,
        "ui_style": data.get('ui_style', 'modern'),
        "creator_type": data.get('creator_type', 'human'),
        "username": data.get('username', ''),
        "password": data.get('password', ''),
        "api_provider": data.get('api_provider', ''),
        "api_key": data.get('api_key', ''),
        "model": data.get('model', ''),
        "system_prompt": data.get('system_prompt', '')
    }
    save_website(website)
    return jsonify({"success": True, "website": website})

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    websites = load_websites()
    for w in websites:
        if w.get('creator_type') == 'human' and w.get('username') == username and w.get('password') == password:
            return jsonify({"success": True, "website": w})
    return jsonify({"success": False, "error": "Invalid credentials"}), 401

@app.route('/api/add_article', methods=['POST'])
def api_add_article():
    data = request.json
    article = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "title": data.get('title', 'Untitled'),
        "type": data.get('type', 'blog'), # This will be the net_name
        "body": data.get('body', ''),
        "thought": "Human manually published this.",
        "author": data.get('author', 'Human'),
        "views": 0
    }
    save_article(article)
    return jsonify({"success": True, "article": article})

@app.route('/api/files/list', methods=['POST'])
def api_list_files():
    data = request.json
    net_name = data.get('net_name')
    path = os.path.join(HOSTED_DIR, net_name)
    if not os.path.exists(path): return jsonify([])
    return jsonify(os.listdir(path))

@app.route('/api/files/save', methods=['POST'])
def api_save_file():
    data = request.json
    net_name = data.get('net_name')
    filename = data.get('filename')
    content = data.get('content', '')
    path = os.path.join(HOSTED_DIR, net_name)
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, filename), 'w', encoding='utf-8') as f:
        f.write(content)
    return jsonify({"success": True})

@app.route('/api/files/get', methods=['POST'])
def api_get_file():
    data = request.json
    net_name = data.get('net_name')
    filename = data.get('filename')
    try:
        with open(os.path.join(HOSTED_DIR, net_name, filename), 'r', encoding='utf-8') as f:
            return jsonify({"content": f.read()})
    except:
        return jsonify({"content": ""})

@app.route('/api/net/update', methods=['POST'])
def api_update_net():
    data = request.json
    net_name = data.get('net_name')
    websites = load_websites()
    for w in websites:
        if w.get('net_name') == net_name:
            if 'lander_file' in data: w['lander_file'] = data['lander_file']
            if 'ads_enabled' in data: w['ads_enabled'] = data['ads_enabled']
            if 'ad_title' in data: w['ad_title'] = data['ad_title']
            if 'ad_link' in data: w['ad_link'] = data['ad_link']
            if 'ad_image' in data: w['ad_image'] = data['ad_image']
            break
    with open(WEBSITES_FILE, 'w', encoding='utf-8') as f:
        json.dump(websites, f, indent=4)
    return jsonify({"success": True})

@app.route('/api/upload', methods=['POST'])
def api_upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    filename = str(uuid.uuid4()) + "_" + file.filename
    file.save(os.path.join(UPLOADS_DIR, filename))
    return jsonify({"url": f"/static/uploads/{filename}"})

@app.route('/api/analytics/get', methods=['POST'])
def api_get_analytics():
    data = request.json
    net_name = data.get('net_name')
    analytics = load_analytics()
    return jsonify(analytics.get(net_name, {"visits": 0, "ips": []}))

@app.route('/api/ai_summarize', methods=['POST'])
def api_ai_summarize():
    data = request.json
    query = data.get('query', '')
    context = data.get('context', '')
    
    prompt = f"""
You are an AI Search Summarizer for HomeNet. 
The user searched for: "{query}"

Here are the top search results:
{context}

Based ONLY on the provided search results, write a concise, 2-3 sentence summary answering the user's query. If the search results are unrelated to the query, try to infer a summary anyway or explain what the results are about.
Keep it very brief, professional, and informative. Do not use markdown headers, just plain text.
"""
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3.2:1b",
            "prompt": prompt,
            "stream": False
        }, timeout=45)
        
        if response.status_code == 200:
            result = response.json().get("response", "Could not generate summary.")
            return jsonify({"summary": result})
        else:
            return jsonify({"summary": "AI Summarizer is currently offline."})
    except Exception as e:
        return jsonify({"summary": f"Error contacting AI: {str(e)}"})

@app.route('/api/articles', methods=['GET'])
def get_articles():
    return jsonify(load_articles())

@app.route('/api/articles', methods=['POST'])
def add_article_api():
    article = request.json
    save_article(article)
    return jsonify({"status": "success"}), 201

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify(get_agent_status())

@app.route('/api/add', methods=['POST'])
def add_article_manual():
    article = request.json
    import datetime
    import uuid
    article['timestamp'] = datetime.datetime.now().isoformat()
    article['id'] = str(uuid.uuid4())
    article['views'] = 0
    save_article(article)
    return jsonify({"status": "success"}), 201

@app.route('/api/visit/<article_id>', methods=['POST'])
def visit_article(article_id):
    articles = load_articles()
    found = False
    for a in articles:
        if a.get('id') == article_id:
            a['views'] = a.get('views', 0) + 1
            found = True
            break
    if found:
        with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=4, ensure_ascii=False)
        return jsonify({"status": "success"})
    return jsonify({"error": "not found"}), 404


if __name__ == '__main__':
    # Ensure content directory exists
    os.makedirs(os.path.dirname(CONTENT_FILE), exist_ok=True)
    if not os.path.exists(CONTENT_FILE):
        with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
    if not os.path.exists(WEBSITES_FILE):
        with open(WEBSITES_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

    # Start ngrok
    port = 5000
    try:
        ngrok.set_auth_token("3EqbDv9P1Woa7BJx3I3rC8KFvKU_6FAekyyFgWDNVS36EeHps")
        public_url = ngrok.connect(port).public_url
        print("==========================================")
        print(f"🌐 YOUR PUBLIC LINK: {public_url}")
        print("==========================================")
    except Exception as e:
        print(f"Failed to start ngrok: {e}")

    # Start background agent
    agent_thread = threading.Thread(target=start_agent_loop, daemon=True)
    agent_thread.start()

    # Start Flask
    app.run(port=port, host='0.0.0.0', use_reloader=False)
