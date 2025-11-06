from aurora.agents.base import AuroraAgent
from aurora.core.registry import register
TEMPLATE = '''You are the Prompt Optimizer of Aurora (on the path to SURPA).
MISSION: Turn any instruction into a precise, contextual, and executable prompt.
Constraints:
- Be unambiguous and minimal.
- Include role, task, constraints, success criteria, inputs, outputs.
- Align with Aurora's objective: {objective}.
'''
class AgentImpl(AuroraAgent):
    role = "Chief Prompt Architect"
    def __init__(self):
        super().__init__(name="prompt_optimizer",
                         description="Refines prompts across the organization.")
    def run(self, payload: dict) -> dict:
        ask = payload.get("ask", "")
        prompt = TEMPLATE.format(objective=self.settings.objective).strip() + "\n\nUSER_ASK:\n" + ask
        return {"agent": self.name, "prompt": prompt, "notes": "Ready to use or to send to a specific unit."}
agent = AgentImpl()
register(agent)
