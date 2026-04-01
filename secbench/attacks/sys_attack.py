from abc import abstractmethod
from typing import Iterable, List, Optional

from secbench.attacks.base_attack import BaseAttack
from secbench.types.schemas import AttackContext, AttackResult


class SysBaseAttack(BaseAttack):
    """
    系统层攻击的统一中间抽象层。负责处理注入目标筛选，后续同学在其上扩展具体实现。
    """

    def __init__(
        self,
        attack_name: str,
        target_step_ids: Optional[Iterable[int]] = None,
        target_xml_keywords: Optional[Iterable[str]] = None,
    ):
        super().__init__(attack_name=attack_name)
        self.target_step_ids: List[int] = list(target_step_ids or [])
        self.target_xml_keywords: List[str] = list(target_xml_keywords or [])

    def should_attack(self, context: AttackContext) -> bool:
        if self.target_step_ids and context.step_id not in self.target_step_ids:
            return False

        xml_snapshot = str(context.extra.get("xml", ""))
        if self.target_xml_keywords and not any(
            keyword in xml_snapshot for keyword in self.target_xml_keywords
        ):
            return False

        return True

    @abstractmethod
    def apply(self, image, context: AttackContext) -> AttackResult:
        raise NotImplementedError
