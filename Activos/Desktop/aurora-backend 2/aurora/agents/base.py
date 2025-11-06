from aurora.core.registry import Agent, register
from aurora.knowledge.store import search
from aurora.core.config import get_settings
class AuroraAgent(Agent):
    role: str = "Generic"
    def __init__(self, name: str, description: str):
        self.name = name; self.description = description; self.settings = get_settings()
    def context(self, query: str = "") -> list[dict]:
        return search(query or self.settings.objective)
    def run(self, payload: dict) -> dict:
        q = payload.get("query", "")
        return {"agent": self.name, "role": self.role, "objective": self.settings.objective,
                "input": payload, "context": self.context(q), "output": f"{self.name} received payload."}
