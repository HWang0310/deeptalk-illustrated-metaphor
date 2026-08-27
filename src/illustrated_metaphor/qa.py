"""Evidence-based checks for local prototype manifests."""

from pathlib import Path


def run_qa(asset_manifest: dict) -> dict:
    """Check the claims V0 can establish without an image-generation model."""
    failures = []
    if asset_manifest.get("track") == "a_reference" and not asset_manifest.get("provenance"):
        failures.append("Track A requires upstream-reference provenance")
    if asset_manifest.get("track") in {"b_paper_relay", "b_object_theatre"} and asset_manifest.get("provenance") != "original-language-hypothesis":
        failures.append("Track B candidate requires original-language provenance")
    duration = asset_manifest.get("duration_seconds")
    if not isinstance(duration, (int, float)) or not 3 <= duration <= 10:
        failures.append("duration is outside 3–10 seconds")
    files = asset_manifest.get("files", [])
    if files and any(not Path(file_path).exists() for file_path in files):
        failures.append("one or more declared asset files are missing")
    if not asset_manifest.get("state_names"):
        failures.append("state continuity cannot be checked without ordered states")
    return {"passed": not failures, "failures": failures, "checks": ["provenance", "duration", "files", "state continuity"]}
