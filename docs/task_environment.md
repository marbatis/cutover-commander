# Task Environment

## 1. Rational objective
Assess synthetic cutover readiness with deterministic policy.

## 2. PEAS
- Performance: readiness score quality, explicit blockers, valid GO/CAUTION/HOLD.
- Environment: synthetic migration plans.
- Actuators: report generation only.
- Sensors: plan fields, task dependencies, rehearsal and rollback signals.

## 3. Environmental dimensions
Partially observable, high-impact, sequential and constrained by time windows.

## 4. Problem formalization
Given a cutover plan, compute dependency order, critical path, blockers, and policy decision.

## 5. Architecture choice
FastAPI + SQLAlchemy + deterministic services.

## 6. Guardrails / workflow maturity
Read-only recommendation system, explicit rollback and reconciliation checks.
