from __future__ import annotations

import json
from pathlib import Path

from app.schemas import CutoverPlan


class PlanLoader:
    def __init__(self, root: str = "data/sample_plans"):
        self.root = Path(root)

    def load_sample(self, sample_id: str) -> CutoverPlan:
        path = self.root / f"{sample_id}.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        return CutoverPlan.model_validate(payload)

    def load_payload(self, payload: dict) -> CutoverPlan:
        return CutoverPlan.model_validate(payload)
