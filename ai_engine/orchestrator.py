import threading, time, random
from ai_engine.generators import generate_local_article, generate_api_article
from ai_engine.utils import get_websites
from ai_engine.logger import log_info

active = set()

def local_loop():
    c = 1
    log_info("Orchestrator", "Local Loop Started")
    while True:
        generate_local_article(c)
        c += 1
        time.sleep(random.randint(15, 30))

def api_loop(w):
    c = 1
    log_info("Orchestrator", f"API Agent Started: {w.get('net_name')}")
    while True:
        generate_api_article(w, c)
        c += 1
        time.sleep(random.randint(60, 120))

def start_engine():
    def monitor():
        while True:
            for w in get_websites():
                if w.get('creator_type') == 'ai' and w.get('id') not in active:
                    threading.Thread(target=api_loop, args=(w,), daemon=True).start()
                    active.add(w.get('id'))
            time.sleep(10)
    threading.Thread(target=monitor, daemon=True).start()
    local_loop()
