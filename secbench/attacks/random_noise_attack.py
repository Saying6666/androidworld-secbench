import random
from typing import Any, Iterable, Optional

from secbench.attacks.sys_attack import SysBaseAttack
from secbench.types.schemas import AttackContext, AttackResult

try:
    import numpy as np
except ImportError:  # pragma: no cover - optional dependency during static setup
    np = None

try:
    from PIL import Image
except ImportError:  # pragma: no cover - optional dependency during static setup
    Image = None


class RandomNoiseAttack(SysBaseAttack):
    """
    随机噪声攻击的实现。
    """

    def __init__(
        self,
        sigma: float = 8.0,
        mode: str = "gaussian",
        target_step_ids: Optional[Iterable[int]] = None,
        target_xml_keywords: Optional[Iterable[str]] = None,
    ):
        super().__init__(
            attack_name="random_noise_attack",
            target_step_ids=target_step_ids,
            target_xml_keywords=target_xml_keywords,
        )
        self.sigma = sigma
        self.mode = mode

    def apply(self, image: Any, context: AttackContext) -> AttackResult:
        params = {
            "mode": self.mode,
            "sigma": self.sigma,
            "target_step_ids": self.target_step_ids,
            "target_xml_keywords": self.target_xml_keywords,
        }

        if not self.should_attack(context):
            return AttackResult(
                attacked_image=image,
                attack_params=params,
                success=False,
                extra={"message": "RandomNoiseAttack skipped because target was not matched."},
            )

        attacked_image = self._apply_noise(image=image, context=context)
        return AttackResult(
            attacked_image=attacked_image,
            attack_params=params,
            success=True,
            extra={"message": "RandomNoiseAttack injected noise successfully."},
        )

    def _apply_noise(self, image: Any, context: AttackContext):
        seed = context.attack_seed + (context.step_id or 0)

        if np is not None and Image is not None and hasattr(image, "mode") and hasattr(image, "size"):
            image_array = np.asarray(image).astype(np.float32)
            attacked = self._inject_gaussian_noise(image_array, seed)
            return Image.fromarray(attacked)

        if np is not None and isinstance(image, np.ndarray):
            return self._inject_gaussian_noise(image.astype(np.float32), seed)

        token = random.Random(seed).randint(1000, 9999)
        return (
            f"{image}|random_noise(mode={self.mode},sigma={self.sigma},"
            f"seed={seed},token={token})"
        )

    def _inject_gaussian_noise(self, image_array, seed: int):
        if np is None:
            return image_array

        rng = np.random.default_rng(seed)
        noise = rng.normal(loc=0.0, scale=self.sigma, size=image_array.shape)
        attacked = np.clip(image_array + noise, 0, 255).astype(np.uint8)
        return attacked
