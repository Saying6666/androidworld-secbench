def _terminal_results(results):
    terminals = [result for result in results if result.get("done", False)]
    if terminals:
        return terminals

    if not results:
        return []

    return [results[-1]]


def task_success_rate(results):
    terminals = _terminal_results(results)
    if not terminals:
        return 0.0
    success_count = sum(1 for x in terminals if x.get("task_success", False))
    return success_count / len(terminals)


def mean_episode_length(results):
    successful_terminals = [
        terminal for terminal in _terminal_results(results)
        if terminal.get("task_success", False)
    ]
    lengths = [x.get("episode_length", 0) for x in successful_terminals]
    if not lengths:
        return 0.0
    return sum(lengths) / len(lengths)
