from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import api_router, web_router
from app.db import init_db
from app.logging_config import configure_logging

configure_logging()
app = FastAPI(title="Cutover Commander", version="0.1.0")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(web_router)
app.include_router(api_router)


@app.on_event("startup")
def startup() -> None:
    init_db()
