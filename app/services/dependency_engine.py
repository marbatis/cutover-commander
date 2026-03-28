from __future__ import annotations

from collections import defaultdict, deque

from app.schemas import CutoverTask


def topological_order(tasks: list[CutoverTask]) -> tuple[list[str], bool]:
    task_ids = {task.task_id for task in tasks}
    indegree: dict[str, int] = {task.task_id: 0 for task in tasks}
    graph: dict[str, list[str]] = defaultdict(list)

    for task in tasks:
        for dep in task.depends_on:
            if dep in task_ids:
                graph[dep].append(task.task_id)
                indegree[task.task_id] += 1

    queue = deque(sorted([task_id for task_id, degree in indegree.items() if degree == 0]))
    ordered: list[str] = []

    while queue:
        node = queue.popleft()
        ordered.append(node)
        for nxt in sorted(graph[node]):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    has_cycle = len(ordered) != len(tasks)
    return ordered, has_cycle
