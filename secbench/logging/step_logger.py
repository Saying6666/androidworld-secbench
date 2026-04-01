import json
from pathlib import Path


class StepLogger:
    def __init__(self, output_dir: str = "outputs/steps"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def log(self, run_id: str, step_id: int, payload: dict):
        save_path = self.output_dir / f"step_{step_id:04d}.json"
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
        return str(save_path)
