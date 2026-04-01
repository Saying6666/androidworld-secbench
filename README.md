# AndroidWorld-SecBench

## 项目简介

本项目是一个面向 Android 手机智能体的安全评测平台。

当前完成了以下初始化任务：

* 仓库初始化
* 目录结构管理
* 统一运行入口
* 最小运行链路

---

## 项目结构

```text
androidworld-secbench/
├── docs/
│   └── attacks.md              # 攻击接口文档
├── runner.py                  # 程序入口
├── configs/                   # 配置文件
│   └── default.yaml
├── scripts/                   # 运行脚本
│   └── run.sh
├── secbench/
│   ├── agents/                # agent 实现
│   │   ├── base_agent.py
│   │   └── mock_agent.py
│   ├── attacks/               # 攻击模块
│   │   ├── base_attack.py
│   │   ├── sys_attack.py
│   │   ├── random_noise_attack.py
│   │   └── dummy_attack.py
│   ├── envs/                  # 环境模块
│   │   ├── base_attack_env.py
│   │   ├── sys_attacked_env.py
│   │   ├── random_noise_attack_env.py
│   │   └── mock_androidworld_env.py
│   ├── logging/               # 日志模块
│   │   ├── run_logger.py
│   │   ├── step_logger.py
│   │   └── image_logger.py
│   ├── metrics/               # 评测指标
│   │   ├── core.py
│   │   ├── aggregate.py
│   │   └── compare.py
│   ├── types/                 # 数据结构
│   │   └── schemas.py
│   └── utils/                 # 工具
│       └── factory.py
└── outputs/
    ├── runs/                  # 实验日志
    ├── steps/                 # 步骤日志
    └── reports/               # 报告
```

---

## 环境安装

```bash
pip install -r requirements.txt
```

---

## 快速开始

默认配置运行：

```bash
bash scripts/run.sh
```

指定配置运行：

```bash
python3 runner.py --config configs/default.yaml
```

运行后将自动生成以下内容：

* 实验日志：`outputs/runs/`
* 步骤日志：`outputs/steps/`
* 报告：`outputs/reports/`

---

## 当前阶段初始化内容

* 使用 `runner.py` 作为统一运行入口，通过配置文件驱动
* 使用 `scripts/run.sh` 作为启动脚本
*  `BaseAttack -> SysBaseAttack -> RandomNoiseAttack` 
*  `BaseAttackEnv -> SysAttackedEnv -> RandomNoiseAttackEnv` 
* 预留 `agent / metrics / docs / outputs` 目录
* 使用 `MockAndroidWorldEnv + MockAgent + RandomNoiseAttack` 构成最小示例

---

## 配置说明

默认配置文件为 [configs/default.yaml](configs/default.yaml)。

其中核心字段包括：

* `run.output_root`：统一输出根目录
* `task.name`：任务名称
* `env.base`：基础环境名称
* `env.wrapper`：包装环境名称
* `agent.name`：agent 名称
* `attack.name`：攻击名称
* `attack.enabled`：是否启用攻击
* `attack.inject_on_reset`：是否在 reset 注入
* `attack.inject_on_step`：是否在 step 注入
* `logging.save_raw_images`：是否保存原始图片或占位产物
* `logging.save_attacked_images`：是否保存攻击后图片或占位产物

---

## 预留的团队接入点

* 攻击同学在 [secbench/attacks/random_noise_attack.py](secbench/attacks/random_noise_attack.py) 或新增攻击文件中补充真实攻击逻辑
* 环境同学将 [secbench/envs/mock_androidworld_env.py](secbench/envs/mock_androidworld_env.py) 替换为真实 AndroidWorld 环境
* 指标同学完善 [secbench/metrics/core.py](secbench/metrics/core.py)、[secbench/metrics/aggregate.py](secbench/metrics/aggregate.py)、[secbench/metrics/compare.py](secbench/metrics/compare.py)
* 文档说明集中在 [docs/attacks.md](docs/attacks.md)
