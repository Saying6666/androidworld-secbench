from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from secbench.agents import MockAgent
from secbench.attacks import DummyAttack, RandomNoiseAttack
from secbench.envs import MockAndroidWorldEnv, RandomNoiseAttackEnv, SysAttackedEnv

DEFAULT_CONFIG = {
    "run": {
        "run_id": "",
        "output_root": "outputs",
        "attack_seed": 42,
        "max_steps": 5,
    },
    "task": {
        "name": "demo_task",
        "success_on_complete": True,
    },
    "env": {
        "base": "mock_androidworld",
        "wrapper": "sys_attacked_env",
        "params": {},
    },
    "agent": {
        "name": "mock_agent",
        "params": {
            "action_prefix": "mock_action",
        },
    },
    "attack": {
        "name": "dummy_attack",
        "enabled": True,
        "inject_on_reset": True,
        "inject_on_step": True,
        "params": {},
    },
    "logging": {
        "save_raw_images": True,
        "save_attacked_images": True,
    },
}

BASE_ENV_REGISTRY = {
    "mock_androidworld": MockAndroidWorldEnv,
}

WRAPPER_ENV_REGISTRY = {
    "sys_attacked_env": SysAttackedEnv,
    "random_noise_attack_env": RandomNoiseAttackEnv,
}

ATTACK_REGISTRY = {
    "dummy_attack": DummyAttack,
    "random_noise_attack": RandomNoiseAttack,
}

AGENT_REGISTRY = {
    "mock_agent": MockAgent,
}


def _deep_merge(base, override):
    merged = deepcopy(base)
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def normalize_config(raw_config):
    return _deep_merge(DEFAULT_CONFIG, raw_config or {})


def resolve_run_id(requested_run_id):
    if requested_run_id:
        return str(requested_run_id)

    return datetime.now(timezone.utc).strftime("run_%Y%m%dT%H%M%SZ")


def build_output_paths(cfg, run_id):
    output_root = Path(cfg["run"]["output_root"])
    runs_dir = output_root / "runs"
    steps_dir = output_root / "steps" / run_id
    reports_dir = output_root / "reports" / run_id

    for directory in (runs_dir, steps_dir, reports_dir):
        directory.mkdir(parents=True, exist_ok=True)

    return {
        "output_root": output_root,
        "runs_dir": runs_dir,
        "steps_dir": steps_dir,
        "reports_dir": reports_dir,
    }


def build_base_env(cfg):
    env_name = cfg["env"]["base"]
    env_cls = BASE_ENV_REGISTRY.get(env_name)
    if env_cls is None:
        raise ValueError(f"Unsupported base env: {env_name}")

    env_params = dict(cfg["env"].get("params", {}))
    env_params.update(
        {
            "task_name": cfg["task"]["name"],
            "max_steps": cfg["run"]["max_steps"],
            "success_on_complete": cfg["task"].get("success_on_complete", True),
        }
    )
    return env_cls(**env_params)


def build_attack(cfg):
    attack_name = cfg["attack"]["name"]
    attack_cls = ATTACK_REGISTRY.get(attack_name)
    if attack_cls is None:
        raise ValueError(f"Unsupported attack: {attack_name}")

    attack_params = dict(cfg["attack"].get("params", {}))
    return attack_cls(**attack_params)


def build_agent(cfg):
    agent_name = cfg["agent"]["name"]
    agent_cls = AGENT_REGISTRY.get(agent_name)
    if agent_cls is None:
        raise ValueError(f"Unsupported agent: {agent_name}")

    return agent_cls(**cfg["agent"].get("params", {}))


def build_env(cfg, base_env, attack):
    wrapper_name = cfg["env"]["wrapper"]
    wrapper_cls = WRAPPER_ENV_REGISTRY.get(wrapper_name)
    if wrapper_cls is None:
        raise ValueError(f"Unsupported wrapper env: {wrapper_name}")

    return wrapper_cls(
        base_env=base_env,
        attack=attack,
        enabled=cfg["attack"]["enabled"],
        inject_on_reset=cfg["attack"]["inject_on_reset"],
        inject_on_step=cfg["attack"]["inject_on_step"],
    )
