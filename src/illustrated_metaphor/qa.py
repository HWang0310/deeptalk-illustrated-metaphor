"""Evidence-based checks for local prototype manifests."""

from pathlib import Path

from .common_briefs import REVIEW_FIELDS


def run_qa(asset_manifest: dict) -> dict:
    """Check the claims V0 can establish without an image-generation model."""
    failures = []
    if asset_manifest.get("track") == "a_reference" and not asset_manifest.get("provenance"):
        failures.append("Track A requires upstream-reference provenance")
    if asset_manifest.get("track") in {"b_paper_relay", "b_object_theatre"} and asset_manifest.get("provenance") != "original-language-hypothesis":
        failures.append("Track B candidate requires original-language provenance")
    if asset_manifest.get("track") == "b1_metaphor_system":
        if asset_manifest.get("provenance") != "original-metaphor-system":
            failures.append("V0.2 system requires original-metaphor-system provenance")
        visual = asset_manifest.get("visual_qa", {})
        if not isinstance(visual.get("focal_object"), str) or not visual["focal_object"].strip():
            failures.append("V0.2 system requires a focal object")
        if not isinstance(visual.get("object_count"), int) or not 1 <= visual["object_count"] <= 4:
            failures.append("V0.2 object count must remain between 1 and 4")
        if not isinstance(visual.get("annotation_count"), int) or not 1 <= visual["annotation_count"] <= 2:
            failures.append("V0.2 annotation density must remain sparse")
        if visual.get("uses_actor") and not visual.get("actor_object_separation"):
            failures.append("V0.2 actor and objects must remain separable")
        if visual.get("clutter_candidate"):
            failures.append("V0.2 composition is flagged as a clutter candidate")
        if visual.get("final_frame_readability") != "candidate":
            failures.append("V0.2 final frame lacks a structural readability candidate")
    if asset_manifest.get("study") == "common-brief-trial":
        review = asset_manifest.get("trial_review")
        if not isinstance(review, dict) or not REVIEW_FIELDS.issubset(review):
            failures.append("Common Brief trial requires a complete review rubric")
        elif review.get("suitability") not in {"SUITABLE", "BORDERLINE"}:
            failures.append("Common Brief candidate suitability must be SUITABLE or BORDERLINE")
        elif review.get("track") != "b1_metaphor_system":
            failures.append("Common Brief candidate must remain on the B1 primary track")
    duration = asset_manifest.get("duration_seconds")
    if not isinstance(duration, (int, float)) or not 3 <= duration <= 10:
        failures.append("duration is outside 3–10 seconds")
    files = asset_manifest.get("files", [])
    if files and any(not Path(file_path).exists() for file_path in files):
        failures.append("one or more declared asset files are missing")
    if not asset_manifest.get("state_names"):
        failures.append("state continuity cannot be checked without ordered states")
    return {"passed": not failures, "failures": failures, "checks": ["provenance", "duration", "files", "state continuity", "focal clarity", "object count", "annotation density", "actor/object separation", "clutter candidate", "final-frame readability", "common brief rubric"]}
