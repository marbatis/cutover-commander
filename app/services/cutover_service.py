from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.repositories.report_repo import ReportRepository
from app.schemas import CutoverPlan, CutoverReport, CutoverResponse
from app.services.readiness_policy import evaluate_plan
from app.services.reporting import build_memo


class CutoverService:
    def __init__(self, repo: ReportRepository):
        self.repo = repo

    def assess(self, plan: CutoverPlan) -> CutoverResponse:
        outcome = evaluate_plan(plan)
        report = CutoverReport(
            report_id=f"cutover_{uuid4().hex[:10]}",
            cutover_id=plan.cutover_id,
            readiness_score=outcome["readiness_score"],
            decision=outcome["decision"],
            blockers=outcome["blockers"],
            critical_path=outcome["critical_path"],
            rollback_triggers=outcome["rollback_triggers"],
            missing_rehearsals=outcome["missing_rehearsals"],
            reconciliation_watchlist=outcome["reconciliation_watchlist"],
            memo=build_memo(plan.cutover_id, outcome["decision"], outcome["readiness_score"], outcome["blockers"]),
            created_at=datetime.now(timezone.utc),
        )
        response = CutoverResponse(report=report, plan=plan)
        self.repo.save(report.report_id, plan.cutover_id, response.model_dump_json())
        return response

    def get(self, report_id: str) -> CutoverResponse | None:
        data = self.repo.get(report_id)
        return CutoverResponse.model_validate(data) if data else None

    def history(self) -> list[CutoverResponse]:
        return [CutoverResponse.model_validate(item) for item in self.repo.list_recent()]
