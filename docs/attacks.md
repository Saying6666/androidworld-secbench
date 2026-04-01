# attacks.md

## 文档目标

本文档用于统一 AndroidWorld-SecBench 中攻击接口的命名、输入输出和扩展方式。

## 数据结构

### AttackContext

定义位置：
[secbench/types/schemas.py](../secbench/types/schemas.py)

字段说明：

* `run_id: str` 当前实验运行 ID
* `task_name: str` 当前任务名称
* `attack_seed: int` 攻击随机种子
* `agent_name: str` 当前 agent 名称
* `step_id: Optional[int]` 当前步骤编号
* `extra: Dict[str, Any]` 额外上下文


### AttackResult

定义位置：
[secbench/types/schemas.py](../secbench/types/schemas.py)

字段说明：

* `attacked_image: Any` 攻击后图像对象
* `attack_params: Dict[str, Any]` 攻击参数快照
* `success: bool` 本次攻击是否实际注入
* `extra: Dict[str, Any]` 额外信息

用途：

* 作为攻击统一返回值
* 支撑 step 日志、run 日志和报告存储

## 抽象基类

### BaseAttack

定义位置：
[secbench/attacks/base_attack.py](../secbench/attacks/base_attack.py)


### SysBaseAttack

定义位置：
[secbench/attacks/sys_attack.py](../secbench/attacks/sys_attack.py)


## 已预留攻击类

### RandomNoiseAttack

定义位置：
[secbench/attacks/random_noise_attack.py](../secbench/attacks/random_noise_attack.py)


## 运行顺序

统一运行入口：
[runner.py](../runner.py)

运行步骤：

1. 读取配置文件
2. 创建基础环境 `base_env`
3. 创建攻击对象 `attack`
4. 创建 logger
5. 创建包装环境 `env`
6. 创建 agent
7. 执行循环
8. 存储日志和图片产物
