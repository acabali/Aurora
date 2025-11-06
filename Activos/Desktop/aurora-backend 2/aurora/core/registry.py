from typing import Dict
class Agent:
    name: str = "agent"
    description: str = ""
    def run(self, payload: dict) -> dict: raise NotImplementedError
_registry: Dict[str, Agent] = {}
def register(agent: Agent): _registry[agent.name] = agent
def get(name: str) -> Agent: return _registry[name]
def list_agents() -> list[str]: return sorted(_registry.keys())
