from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional


@dataclass
class AttackContext:
    run_id: str
    task_name: str
    attack_seed: int
    agent_name: str
    step_id: Optional[int] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AttackResult:
    attacked_image: Any = None
    attack_params: Dict[str, Any] = field(default_factory=dict)
    success: bool = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_metadata(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload.pop("attacked_image", None)
        return payload
