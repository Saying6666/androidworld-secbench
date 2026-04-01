from secbench.attacks.sys_attack import SysBaseAttack
from secbench.types.schemas import AttackContext, AttackResult


class DummyAttack(SysBaseAttack):
    def __init__(self, target_step_ids=None, target_xml_keywords=None):
        super().__init__(
            attack_name="dummy_attack",
            target_step_ids=target_step_ids,
            target_xml_keywords=target_xml_keywords,
        )

    def apply(self, image, context: AttackContext) -> AttackResult:
        if not self.should_attack(context):
            return AttackResult(
                attacked_image=image,
                attack_params={"mode": "no_op"},
                success=False,
                extra={"message": "Dummy attack skipped because target was not matched."},
            )

        return AttackResult(
            attacked_image=image,
            attack_params={"mode": "no_op"},
            success=False,
            extra={"message": "Dummy attack does not modify image."}
        )
