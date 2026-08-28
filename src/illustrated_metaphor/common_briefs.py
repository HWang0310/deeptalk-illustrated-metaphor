"""Fixed Common Brief trial definitions for the Illustrated Metaphor experiment."""

import json
from pathlib import Path


REQUIRED_FIELDS = {
    "id", "title", "spoken_semantics", "visual_purpose", "suitability", "candidate", "track",
    "visual_case_id", "route", "candidate_text", "reason", "semantic_clarity", "metaphor_clarity",
    "time_to_understand", "family_naturalness", "emotional_agency_usefulness", "motion_usefulness",
    "chinese_readability", "clutter", "creator_usefulness", "generic_actor", "object_only", "metaphor_overreach",
}

REVIEW_FIELDS = REQUIRED_FIELDS - {"spoken_semantics", "visual_purpose", "candidate_text"}


def load_common_briefs(path: str = "benchmarks/common-briefs.json") -> list[dict]:
    """Load the fixed eight-item comparison experiment without altering its semantics."""
    briefs = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(briefs, list):
        raise ValueError("common briefs must be a JSON array")
    expected_ids = [f"CB{number:02d}" for number in range(1, 9)]
    if [brief.get("id") for brief in briefs] != expected_ids:
        raise ValueError("common briefs must contain ordered CB01–CB08")
    for brief in briefs:
        missing = REQUIRED_FIELDS - set(brief)
        if missing:
            raise ValueError("common brief missing fields: " + ", ".join(sorted(missing)))
        if brief["suitability"] not in {"SUITABLE", "BORDERLINE", "ABSTAIN"}:
            raise ValueError(f"invalid suitability: {brief['id']}")
        if brief["candidate"] and (brief["track"] != "b1_metaphor_system" or not brief["visual_case_id"]):
            raise ValueError(f"candidate must use B1 with a visual case: {brief['id']}")
        if not brief["candidate"] and brief["suitability"] != "ABSTAIN":
            raise ValueError(f"only abstentions may omit a candidate: {brief['id']}")
    return briefs
