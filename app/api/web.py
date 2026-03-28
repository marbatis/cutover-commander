from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.report_repo import ReportRepository
from app.services.cutover_service import CutoverService
from app.services.plan_loader import PlanLoader

router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory="app/templates")


def _service(db: Session) -> CutoverService:
    return CutoverService(ReportRepository(db))


@router.get("/")
def home(request: Request):
    samples = ["core_cutover_plan", "blocked_cutover_plan", "caution_cutover_plan"]
    return templates.TemplateResponse("index.html", {"request": request, "samples": samples})


@router.get("/history")
def history(request: Request, db: Session = Depends(get_db)):
    reports = _service(db).history()
    return templates.TemplateResponse("history.html", {"request": request, "reports": reports})


@router.get("/report/{report_id}")
def report_page(report_id: str, request: Request, db: Session = Depends(get_db)):
    report = _service(db).get(report_id)
    return templates.TemplateResponse("detail.html", {"request": request, "item": report})


@router.get("/run/{sample_id}")
def run_sample(sample_id: str, request: Request, db: Session = Depends(get_db)):
    service = _service(db)
    plan = PlanLoader().load_sample(sample_id)
    result = service.assess(plan)
    return templates.TemplateResponse("detail.html", {"request": request, "item": result})
