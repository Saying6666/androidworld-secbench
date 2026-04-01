from abc import ABC, abstractmethod
from secbench.types.schemas import AttackContext, AttackResult


class BaseAttack(ABC):
    def __init__(self, attack_name: str):
        self.attack_name = attack_name

    @abstractmethod
    def apply(self, image, context: AttackContext) -> AttackResult:
        """
        执行攻击，返回 AttackResult
        """
        raise NotImplementedError