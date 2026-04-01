from secbench.envs.base_attack_env import BaseAttackEnv
from secbench.types.schemas import AttackContext


class SysAttackedEnv(BaseAttackEnv):
    def __init__(
        self,
        base_env,
        attack=None,
        enabled: bool = True,
        inject_on_reset: bool = True,
        inject_on_step: bool = True,
    ):
        super().__init__(
            base_env=base_env,
            attack=attack,
            enabled=enabled,
            inject_on_reset=inject_on_reset,
            inject_on_step=inject_on_step,
        )

    def _record_transition(self, raw_obs, attacked_obs, attack_result):
        self.last_raw_observation = dict(raw_obs)
        self.last_attacked_observation = dict(attacked_obs)
        self.last_attack_result = attack_result
        return attacked_obs, attack_result

    def _maybe_attack(self, obs, step_id: int, phase: str):
        if not self.enabled or self.attack is None:
            return self._record_transition(obs, obs, None)

        context = AttackContext(
            run_id=self.run_id or "unknown_run",
            task_name=self.base_env.task_name,
            attack_seed=self.attack_seed,
            agent_name=self.agent_name,
            step_id=step_id,
            extra={
                "phase": phase,
                "xml": obs.get("xml"),
            },
        )

        result = self.attack.apply(obs["image"], context)

        attacked_obs = dict(obs)
        attacked_obs["image"] = result.attacked_image
        attacked_obs["attack_applied"] = result.success
        return self._record_transition(obs, attacked_obs, result)

    def reset(self):
        obs = self.base_env.reset()
        if not self.inject_on_reset:
            return self._record_transition(obs, obs, None)
        return self._maybe_attack(obs, step_id=0, phase="reset")

    def step(self, action):
        obs = self.base_env.step(action)
        step_id = getattr(self.base_env, "current_step", -1)
        if not self.inject_on_step:
            return self._record_transition(obs, obs, None)
        return self._maybe_attack(obs, step_id=step_id, phase="step")
