from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.report_repo import ReportRepository
from app.services.cutover_service import CutoverService
from app.services.plan_loader import PlanLoader

router = APIRouter(prefix="/api", tags=["api"])


def _service(db: Session) -> CutoverService:
    return CutoverService(ReportRepository(db))


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/cutover/sample/{sample_id}")
def assess_sample(sample_id: str, db: Session = Depends(get_db)) -> dict:
    plan = PlanLoader().load_sample(sample_id)
    return _service(db).assess(plan).model_dump(mode="json")


@router.post("/cutover/upload")
async def assess_upload(file: UploadFile = File(...), db: Session = Depends(get_db)) -> dict:
    if file.size and file.size > 1_000_000:
        raise HTTPException(status_code=413, detail="Payload too large")
    payload = await file.read()
    try:
        import json

        data = json.loads(payload.decode("utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid JSON") from exc

    plan = PlanLoader().load_payload(data)
    return _service(db).assess(plan).model_dump(mode="json")


@router.get("/cutover/{report_id}")
def get_report(report_id: str, db: Session = Depends(get_db)) -> dict:
    record = _service(db).get(report_id)
    if not record:
        raise HTTPException(status_code=404, detail="Report not found")
    return record.model_dump(mode="json")
