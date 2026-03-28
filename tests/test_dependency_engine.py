from app.schemas import CutoverTask
from app.services.dependency_engine import topological_order


def test_topological_order() -> None:
    tasks = [
        CutoverTask(task_id="t1", name="a", depends_on=[]),
        CutoverTask(task_id="t2", name="b", depends_on=["t1"]),
    ]
    order, has_cycle = topological_order(tasks)
    assert not has_cycle
    assert order == ["t1", "t2"]
