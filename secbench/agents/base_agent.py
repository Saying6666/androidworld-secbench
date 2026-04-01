from abc import ABC, abstractmethod


class BaseAgent(ABC):
    def __init__(self, agent_name: str):
        self.agent_name = agent_name

    @abstractmethod
    def act(self, observation):
        raise NotImplementedError
