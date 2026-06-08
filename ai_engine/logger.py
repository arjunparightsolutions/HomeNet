def log_info(mod, msg): print(f"[{mod}] INFO: {msg}")
def log_error(mod, err): print(f"[{mod}] ERROR: {err}")
def log_warning(mod, warn): print(f"[{mod}] WARNING: {warn}")
def log_cycle(c, t, e=False): print(f"🤖 Cycle {c} — {'Error' if e else 'Published'}: {t}")
