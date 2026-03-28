from app.schemas import CutoverTask
from app.services.critical_path import compute_critical_path


def test_critical_path() -> None:
    tasks = [
        CutoverTask(task_id="t1", name="a", duration_minutes=10),
        CutoverTask(task_id="t2", name="b", depends_on=["t1"], duration_minutes=40),
        CutoverTask(task_id="t3", name="c", depends_on=["t2"], duration_minutes=20),
    ]
    assert compute_critical_path(tasks) == ["t1", "t2", "t3"]
