"""Benchmark case loading and minimal structural validation."""

import json
from pathlib import Path


REQUIRED_FIELDS = {
    "id",
    "tracks",
    "semantic_intent",
    "metaphor",
    "scene_states",
    "text",
    "duration_seconds",
    "qa_criteria",
}


def load_cases(path: str) -> list[dict]:
    """Load V0 cognitive-metaphor cases and reject malformed benchmark data."""
    cases = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(cases, list):
        raise ValueError("benchmark must be a JSON array")
    ids = set()
    for case in cases:
        missing = REQUIRED_FIELDS - set(case)
        if missing:
            raise ValueError("missing benchmark fields: " + ", ".join(sorted(missing)))
        if case["id"] in ids:
            raise ValueError("benchmark case ids must be unique")
        ids.add(case["id"])
    return cases
