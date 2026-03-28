from __future__ import annotations

from app.schemas import CutoverPlan
from app.services.critical_path import compute_critical_path
from app.services.dependency_engine import topological_order


def evaluate_plan(plan: CutoverPlan) -> dict:
    blockers: list[str] = []
    penalties = 0

    ordered, has_cycle = topological_order(plan.tasks)
    if has_cycle:
        blockers.append("Dependency cycle detected in task graph")
        penalties += 50

    not_ready = [task.task_id for task in plan.tasks if task.status != "ready"]
    if not_ready:
        blockers.append(f"Tasks not ready: {', '.join(not_ready)}")
        penalties += 20

    if plan.freeze_window:
        blockers.append("Freeze window active")
        penalties += 40

    if not plan.rollback_steps:
        blockers.append("Rollback plan is missing")
        penalties += 40

    missing_rehearsals = []
    if not plan.rehearsals_complete:
        missing_rehearsals.append("Rehearsal not complete")
        penalties += 20

    reconciliation_watchlist = []
    if not plan.reconciliation_points:
        reconciliation_watchlist.append("No reconciliation checkpoints defined")
        penalties += 15

    for risk in plan.known_risks:
        if "high" in risk.lower() or "sev" in risk.lower():
            penalties += 5

    readiness_score = max(0.0, min(100.0, 100.0 - float(penalties)))

    if blockers or readiness_score < 60:
        decision = "HOLD"
    elif readiness_score < 80 or missing_rehearsals or reconciliation_watchlist:
        decision = "CAUTION"
    else:
        decision = "GO"

    rollback_triggers = [
        "Error budget burn exceeds threshold",
        "Data reconciliation mismatch exceeds tolerance",
        "Critical dependency health check fails",
    ]

    return {
        "ordered": ordered,
        "critical_path": compute_critical_path(plan.tasks),
        "blockers": blockers,
        "readiness_score": readiness_score,
        "decision": decision,
        "rollback_triggers": rollback_triggers,
        "missing_rehearsals": missing_rehearsals,
        "reconciliation_watchlist": reconciliation_watchlist,
    }
