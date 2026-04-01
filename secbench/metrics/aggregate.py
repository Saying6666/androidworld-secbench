import json
from pathlib import Path


def collect_run_metrics(output_dir: str = "outputs/runs"):
    run_dir = Path(output_dir)
    if not run_dir.exists():
        return []

    metrics_payloads = []
    for path in sorted(run_dir.glob("*.json")):
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        metrics_payloads.append(payload)
    return metrics_payloads


def summarize_metrics(run_payloads):
    if not run_payloads:
        return {}

    summary = {}
    metric_names = sorted({
        metric_name
        for payload in run_payloads
        for metric_name in payload.get("metrics", {}).keys()
    })

    for metric_name in metric_names:
        values = [
            payload["metrics"][metric_name]
            for payload in run_payloads
            if metric_name in payload.get("metrics", {})
        ]
        if values:
            summary[metric_name] = sum(values) / len(values)

    return summary
