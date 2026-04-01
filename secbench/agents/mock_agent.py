from secbench.agents.base_agent import BaseAgent


class MockAgent(BaseAgent):
    def __init__(self, action_prefix: str = "mock_action"):
        super().__init__(agent_name="mock_agent")
        self.action_prefix = action_prefix

    def act(self, observation):
        step_id = observation.get("step_id", 0)
        return f"{self.action_prefix}_{step_id}"
