from __future__ import annotations

import json
from typing import Optional

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models import CutoverReportRecord


class ReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, report_id: str, plan_id: str, report_json: str) -> None:
        self.db.add(CutoverReportRecord(report_id=report_id, plan_id=plan_id, report_json=report_json))
        self.db.commit()

    def get(self, report_id: str) -> Optional[dict]:
        rec = self.db.scalar(select(CutoverReportRecord).where(CutoverReportRecord.report_id == report_id))
        return None if not rec else json.loads(rec.report_json)

    def list_recent(self, limit: int = 25) -> list[dict]:
        rows = self.db.scalars(
            select(CutoverReportRecord).order_by(desc(CutoverReportRecord.created_at)).limit(limit)
        ).all()
        return [json.loads(r.report_json) for r in rows]
