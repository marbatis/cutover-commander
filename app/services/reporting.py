from __future__ import annotations


def build_memo(cutover_id: str, decision: str, readiness_score: float, blockers: list[str]) -> str:
    blocker_text = "; ".join(blockers) if blockers else "No blocking conditions were detected"
    return (
        f"Cutover {cutover_id} readiness is {readiness_score:.1f} with decision {decision}. "
        f"Primary concerns: {blocker_text}."
    )
