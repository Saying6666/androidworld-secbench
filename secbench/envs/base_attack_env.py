from abc import ABC, abstractmethod


class BaseAttackEnv(ABC):
    def __init__(
        self,
        base_env,
        attack=None,
        enabled: bool = True,
        inject_on_reset: bool = True,
        inject_on_step: bool = True,
    ):
        self.base_env = base_env
        self.attack = attack
        self.enabled = enabled
        self.inject_on_reset = inject_on_reset
        self.inject_on_step = inject_on_step

        self.run_id = None
        self.agent_name = "unknown_agent"
        self.attack_seed = 0

        self.last_raw_observation = None
        self.last_attacked_observation = None
        self.last_attack_result = None

    def set_run_meta(self, run_id: str, agent_name: str, attack_seed: int):
        self.run_id = run_id
        self.agent_name = agent_name
        self.attack_seed = attack_seed

    @abstractmethod
    def reset(self):
        """
        重置环境并返回初始 observation
        """
        raise NotImplementedError

    @abstractmethod
    def step(self, action):
        """
        执行动作并返回新的 observation
        """
        raise NotImplementedError
