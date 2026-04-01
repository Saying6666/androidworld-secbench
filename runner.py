import argparse

import yaml

from secbench.logging import ImageLogger, RunLogger, StepLogger
from secbench.metrics.core import mean_episode_length, task_success_rate
from secbench.utils import (
    build_agent,
    build_attack,
    build_base_env,
    build_env,
    build_output_paths,
    normalize_config,
    resolve_run_id,
)


def parse_args():
    parser = argparse.ArgumentParser(description="Run AndroidWorld-SecBench scaffold.")
    parser.add_argument(
        "--config",
        default="configs/default.yaml",
        help="Path to the YAML config file.",
    )
    return parser.parse_args()


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def serialize_attack_result(attack_result):
    if attack_result is None:
        return None
    return attack_result.to_metadata()


def serialize_observation(observation, image_path):
    payload = dict(observation)
    payload["image"] = image_path
    return payload


def infer_artifact_extension(image) -> str:
    if isinstance(image, str):
        return ".txt"

    if hasattr(image, "save") or hasattr(image, "shape"):
        return ".png"

    return ".txt"


def log_step_artifacts(image_logger, step_id, raw_obs, attacked_obs, logging_cfg):
    raw_image = raw_obs.get("image")
    attacked_image = attacked_obs.get("image")
    raw_path = None
    attacked_path = None

    if logging_cfg.get("save_raw_images", True):
        raw_name = f"step_{step_id:04d}_raw{infer_artifact_extension(raw_image)}"
        raw_path = image_logger.log_image(raw_name, raw_image)

    if logging_cfg.get("save_attacked_images", True):
        attacked_name = f"step_{step_id:04d}_attacked{infer_artifact_extension(attacked_image)}"
        attacked_path = image_logger.log_image(attacked_name, attacked_image)

    return raw_path, attacked_path


def build_step_record(
    run_id,
    step_id,
    action,
    mode,
    raw_obs,
    attacked_obs,
    attack_result,
    raw_image_path,
    attacked_image_path,
):
    return {
        "run_id": run_id,
        "step_id": step_id,
        "action": action,
        "mode": mode,
        "raw_image_path": raw_image_path,
        "attacked_image_path": attacked_image_path,
        "success": attack_result.success if attack_result else False,
        "done": attacked_obs.get("done", False),
        "task_success": attacked_obs.get("task_success", False),
        "episode_length": step_id,
        "observation": serialize_observation(attacked_obs, attacked_image_path),
        "raw_observation": serialize_observation(raw_obs, raw_image_path),
        "attack_result": serialize_attack_result(attack_result),
    }


def main():
    args = parse_args()
    cfg = normalize_config(load_config(args.config))
    run_id = resolve_run_id(cfg["run"].get("run_id"))

    task_name = cfg["task"]["name"]
    attack_seed = cfg["run"]["attack_seed"]
    mode = "attacked" if cfg["attack"]["enabled"] else "clean"

    output_paths = build_output_paths(cfg, run_id)
    run_logger = RunLogger(output_dir=str(output_paths["runs_dir"]))
    step_logger = StepLogger(output_dir=str(output_paths["steps_dir"]))
    image_logger = ImageLogger(output_dir=str(output_paths["reports_dir"]))

    base_env = build_base_env(cfg)
    attack = build_attack(cfg)
    agent = build_agent(cfg)
    env = build_env(cfg, base_env=base_env, attack=attack)
    env.set_run_meta(run_id=run_id, agent_name=agent.agent_name, attack_seed=attack_seed)

    step_records = []

    obs, attack_result = env.reset()
    raw_obs = env.last_raw_observation or dict(obs)
    raw_image_path, attacked_image_path = log_step_artifacts(
        image_logger=image_logger,
        step_id=0,
        raw_obs=raw_obs,
        attacked_obs=obs,
        logging_cfg=cfg["logging"],
    )
    reset_record = build_step_record(
        run_id=run_id,
        step_id=0,
        action="reset",
        mode=mode,
        raw_obs=raw_obs,
        attacked_obs=obs,
        attack_result=attack_result,
        raw_image_path=raw_image_path,
        attacked_image_path=attacked_image_path,
    )
    step_logger.log(run_id, 0, reset_record)
    step_records.append(reset_record)

    done = obs.get("done", False)
    step_id = 0

    while not done:
        action = agent.act(obs)
        obs, attack_result = env.step(action)
        step_id += 1
        raw_obs = env.last_raw_observation or dict(obs)
        raw_image_path, attacked_image_path = log_step_artifacts(
            image_logger=image_logger,
            step_id=step_id,
            raw_obs=raw_obs,
            attacked_obs=obs,
            logging_cfg=cfg["logging"],
        )

        record = build_step_record(
            run_id=run_id,
            step_id=step_id,
            action=action,
            mode=mode,
            raw_obs=raw_obs,
            attacked_obs=obs,
            attack_result=attack_result,
            raw_image_path=raw_image_path,
            attacked_image_path=attacked_image_path,
        )
        step_logger.log(run_id, step_id, record)
        step_records.append(record)
        done = obs.get("done", False)

    metrics = {
        "TSR": task_success_rate(step_records),
        "MEL": mean_episode_length(step_records),
    }

    run_payload = {
        "run_id": run_id,
        "task_name": task_name,
        "seed": attack_seed,
        "attack_name": attack.attack_name,
        "agent_name": agent.agent_name,
        "mode": mode,
        "attack_config": cfg["attack"],
        "env_config": cfg["env"],
        "agent_config": cfg["agent"],
        "task_config": cfg["task"],
        "logging_config": cfg["logging"],
        "metrics": metrics,
        "artifacts": {
            "runs_dir": str(output_paths["runs_dir"]),
            "steps_dir": str(output_paths["steps_dir"]),
            "reports_dir": str(output_paths["reports_dir"]),
        },
        "step_count": len(step_records),
    }

    run_path = run_logger.log(run_id, run_payload)

    print("Run finished.")
    print(f"Run log saved to: {run_path}")
    print(f"Step logs saved to: {output_paths['steps_dir']}")
    print(f"Reports saved to: {output_paths['reports_dir']}")
    print(f"Metrics: {metrics}")


if __name__ == "__main__":
    main()
