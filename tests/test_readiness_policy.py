from app.services.plan_loader import PlanLoader
from app.services.readiness_policy import evaluate_plan


def test_blocked_plan_is_hold() -> None:
    plan = PlanLoader().load_sample("blocked_cutover_plan")
    result = evaluate_plan(plan)
    assert result["decision"] == "HOLD"
    assert result["readiness_score"] < 60
