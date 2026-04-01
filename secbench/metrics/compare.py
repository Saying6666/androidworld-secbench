def compare_runs(run_payloads):
    comparisons = []

    for payload in run_payloads:
        comparisons.append(
            {
                "run_id": payload.get("run_id"),
                "task_name": payload.get("task_name"),
                "metrics": payload.get("metrics", {}),
            }
        )

    return comparisons
