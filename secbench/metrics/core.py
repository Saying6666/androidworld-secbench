from __future__ import annotations

from typing import Dict, Iterable, List


def _coerce_results(results: Iterable[Dict]) -> List[Dict]:
    if results is None:
        return []
    return list(results)


def _terminal_results(results: Iterable[Dict]) -> List[Dict]:
    """Return one terminal record per episode.

    AndroidWorld-style evaluation is episode-based: a task rollout ends when the
    environment reports `done=True`. For incomplete traces, we conservatively
    treat the final record as the episode terminus so offline log analysis still
    produces stable metrics.
    """

    records = _coerce_results(results)
    if not records:
        return []

    terminals = [record for record in records if record.get("done", False)]
    if terminals:
        return terminals

    return [records[-1]]


def _safe_average(values: Iterable[float]) -> float:
    values = list(values)
    if not values:
        return 0.0
    return sum(values) / len(values)


def task_success_rate(results: Iterable[Dict]) -> float:
    """Episode success rate.

    TSR = (# successful terminal episodes) / (# terminal episodes)
    """

    terminals = _terminal_results(results)
    if not terminals:
        return 0.0

    success_count = sum(
        1 for terminal in terminals if terminal.get("task_success", False)
    )
    return success_count / len(terminals)


def mean_episode_length(results: Iterable[Dict]) -> float:
    """Average number of action steps for successful episodes only.

    Following the spec, MEL is only computed over successful task completions.
    The stored `episode_length` should represent the number of executed agent
    steps when the episode terminates.
    """

    successful_terminals = [
        terminal
        for terminal in _terminal_results(results)
        if terminal.get("task_success", False)
    ]
    lengths = [terminal.get("episode_length", 0) for terminal in successful_terminals]
    return _safe_average(lengths)


def compute_metrics(results: Iterable[Dict]) -> Dict[str, float]:
    """Compute the spec-required task metrics from step records."""

    return {
        "TSR": task_success_rate(results),
        "MEL": mean_episode_length(results),
    }
