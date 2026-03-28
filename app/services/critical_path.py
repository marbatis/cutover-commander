from __future__ import annotations

from collections import defaultdict

from app.schemas import CutoverTask
from app.services.dependency_engine import topological_order


def compute_critical_path(tasks: list[CutoverTask]) -> list[str]:
    order, has_cycle = topological_order(tasks)
    if has_cycle:
        return []

    by_id = {task.task_id: task for task in tasks}
    graph: dict[str, list[str]] = defaultdict(list)
    distance: dict[str, int] = {task.task_id: by_id[task.task_id].duration_minutes for task in tasks}
    predecessor: dict[str, str] = {}

    for task in tasks:
        for dep in task.depends_on:
            graph[dep].append(task.task_id)

    for node in order:
        for nxt in graph[node]:
            candidate = distance[node] + by_id[nxt].duration_minutes
            if candidate > distance[nxt]:
                distance[nxt] = candidate
                predecessor[nxt] = node

    if not distance:
        return []

    tail = max(distance, key=distance.get)
    path = [tail]
    while tail in predecessor:
        tail = predecessor[tail]
        path.append(tail)
    return list(reversed(path))
