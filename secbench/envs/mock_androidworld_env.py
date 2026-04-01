class MockAndroidWorldEnv:
    def __init__(
        self,
        task_name: str = "demo_task",
        max_steps: int = 5,
        success_on_complete: bool = True,
    ):
        self.task_name = task_name
        self.max_steps = max_steps
        self.success_on_complete = success_on_complete
        self.current_step = 0

    def _build_observation(self, action="reset"):
        done = self.current_step >= self.max_steps
        return {
            "step_id": self.current_step,
            "image": f"raw_image_step_{self.current_step}",
            "text": f"observation after action={action}",
            "xml": f"<screen task='{self.task_name}' step='{self.current_step}' />",
            "done": done,
            "task_success": done and self.success_on_complete,
        }

    def reset(self):
        self.current_step = 0
        return self._build_observation(action="reset")

    def step(self, action):
        self.current_step += 1
        return self._build_observation(action=action)
