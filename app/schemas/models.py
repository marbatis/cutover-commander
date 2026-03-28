from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class CutoverTask(BaseModel):
    task_id: str
    name: str
    depends_on: list[str] = Field(default_factory=list)
    duration_minutes: int = 10
    status: str = "ready"


class CutoverPlan(BaseModel):
    cutover_id: str
    systems: list[str]
    dependencies: list[dict] = Field(default_factory=list)
    tasks: list[CutoverTask]
    windows: list[dict] = Field(default_factory=list)
    checkpoints: list[str] = Field(default_factory=list)
    rollback_steps: list[str] = Field(default_factory=list)
    reconciliation_points: list[str] = Field(default_factory=list)
    owners: list[str] = Field(default_factory=list)
    rehearsals_complete: bool = False
    freeze_window: bool = False
    known_risks: list[str] = Field(default_factory=list)


class CutoverReport(BaseModel):
    report_id: str
    cutover_id: str
    readiness_score: float
    decision: str
    blockers: list[str]
    critical_path: list[str]
    rollback_triggers: list[str]
    missing_rehearsals: list[str]
    reconciliation_watchlist: list[str]
    memo: str
    created_at: datetime


class CutoverResponse(BaseModel):
    report: CutoverReport
    plan: CutoverPlan
