# cutover-commander

Synthetic cutover planning and readiness app for legacy-to-modern migrations.

## Overview
This app evaluates cutover plans with deterministic dependency analysis and readiness policy.

## Why it matters
Cutovers fail when dependency order, rollback readiness, and reconciliation coverage are not explicit.

## Architecture
- Plan loader: `app/services/plan_loader.py`
- Dependency ordering: `app/services/dependency_engine.py`
- Critical path: `app/services/critical_path.py`
- Readiness policy: `app/services/readiness_policy.py`
- Reporting orchestration: `app/services/cutover_service.py`

## Local setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Heroku
`Procfile` and `runtime.txt` are included.

## Mock mode
No OpenAI key required for MVP.

## Roadmap
- Timeline visualization enhancements.
- Multiple plan comparisons.
