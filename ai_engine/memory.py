from ai_engine.utils import get_recent_titles
class AgentMemory:
    def __init__(self, limit=5): self.limit = limit
    def get_context(self):
        titles = get_recent_titles(self.limit)
        return ", ".join(filter(None, titles)) if titles else "No past articles."
