"""Prototype runner; intentionally a natural internal tool rather than a final plugin API."""

import hashlib
import json
from pathlib import Path

from .benchmark import load_cases
from .common_briefs import REVIEW_FIELDS, load_common_briefs
from .motion import build_route
from .qa import run_qa
from .render import assemble_mp4, contact_sheet, render_frame
from .vocabulary import get_metaphor_spec


TRACK_PROVENANCE = {
    "a_reference": "upstream-reference-only",
    "b_neutral": "original-neutral-prototype",
    "b_paper_relay": "original-language-hypothesis",
    "b_object_theatre": "original-language-hypothesis",
    "b1_metaphor_system": "original-metaphor-system",
}


def _render_asset(output: Path, case: dict, track: str, route: str, approved_state_index: int = 0, asset_id: str | None = None, manifest_case_id: str | None = None, metadata: dict | None = None) -> dict:
    plan = build_route(route, case, output)
    state_indexes = [approved_state_index] if route == "approved_still" else list(range(len(case["scene_states"])))
    output_id = asset_id or case["id"]
    recorded_case_id = manifest_case_id or case["id"]
    frame_dir = output / output_id / track / route / "sequence"
    for number, state_index in enumerate(state_indexes, 1):
        render_frame(track, case["text"], state_index, frame_dir / f"frame_{number:03d}.png", case_id=case["id"], display_case_id=recorded_case_id)
    mp4_path = frame_dir.parent / "asset.mp4"
    pattern = str(frame_dir / "frame_%03d.png")
    assemble_mp4(pattern, len(state_indexes), case["duration_seconds"], mp4_path, single_still=plan["source_mode"] == "single_approved_still")
    contact_path = frame_dir.parent / "contact-sheet.png"
    contact_sheet(pattern, len(state_indexes), contact_path)
    files = [str(mp4_path), str(contact_path)] + [str(path) for path in sorted(frame_dir.glob("*.png"))]
    asset = {**plan, "case_id": recorded_case_id, "visual_case_id": case["id"], "track": track, "provenance": TRACK_PROVENANCE[track], "files": files, **(metadata or {})}
    if track == "b1_metaphor_system":
        spec = get_metaphor_spec(case["id"])
        asset["visual_qa"] = {
            "focal_object": spec.focal_object,
            "object_count": len(spec.objects),
            "annotation_count": 1,
            "uses_actor": spec.actor_role is not None,
            "actor_object_separation": True,
            "clutter_candidate": False,
            "final_frame_readability": "candidate",
        }
    asset["sequence_sha256"] = hashlib.sha256(b"".join(Path(item).read_bytes() for item in files[2:])).hexdigest()
    asset["qa"] = run_qa(asset)
    (frame_dir.parent / "manifest.json").write_text(json.dumps(asset, ensure_ascii=False, indent=2), encoding="utf-8")
    return asset


def render_prototypes(output: Path, case_limit: int | None = None) -> dict:
    """Render both tracks across all comparison routes and write evidence metadata."""
    output.mkdir(parents=True, exist_ok=True)
    assets = []
    for case in load_cases("benchmarks/v0-cases.json")[:case_limit]:
        for track in case["tracks"]:
            for route in ("approved_still", "structured_hybrid", "independent_keyframes"):
                assets.append(_render_asset(output, case, track, route))
    result = {"renderer": "ffmpeg local no-key deterministic", "assets": assets}
    (output / "render-manifest.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def render_v01_comparison(output: Path) -> dict:
    """Render the bounded V0.1 visual-language comparison corpus."""
    output.mkdir(parents=True, exist_ok=True)
    routes_by_track = {
        "a_reference": ("approved_still",),
        "b_neutral": ("approved_still",),
        "b_paper_relay": ("approved_still", "structured_hybrid"),
        "b_object_theatre": ("approved_still",),
    }
    assets = []
    for case in load_cases("benchmarks/v0-cases.json"):
        for track, routes in routes_by_track.items():
            for route in routes:
                assets.append(_render_asset(output, case, track, route))
    result = {"renderer": "ffmpeg local no-key deterministic", "study": "v0.1-original-visual-language", "assets": assets}
    (output / "render-manifest.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def render_v02_comparison(output: Path) -> dict:
    """Render the V0.2 four-baseline comparison plus selective state evidence."""
    output.mkdir(parents=True, exist_ok=True)
    selective_state_cases = {"burden-growth", "information-overload", "state-transition"}
    assets = []
    for case in load_cases("benchmarks/v0-cases.json"):
        for track in ("a_reference", "b_paper_relay", "b1_metaphor_system", "b_object_theatre"):
            assets.append(_render_asset(output, case, track, "approved_still", approved_state_index=len(case["scene_states"]) - 1))
        if case["id"] in selective_state_cases:
            assets.append(_render_asset(output, case, "b1_metaphor_system", "structured_hybrid"))
    result = {"renderer": "ffmpeg local no-key deterministic", "study": "v0.2-original-metaphor-system", "assets": assets}
    (output / "render-manifest.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def render_common_brief_trial(output: Path) -> dict:
    """Render only the B1 candidates selected by the fixed Common Brief experiment."""
    output.mkdir(parents=True, exist_ok=True)
    visual_cases = {case["id"]: case for case in load_cases("benchmarks/v0-cases.json")}
    briefs = load_common_briefs()
    assets = []
    for brief in briefs:
        if not brief["candidate"]:
            continue
        visual_case = {**visual_cases[brief["visual_case_id"]], "text": brief["candidate_text"]}
        review = {field: brief[field] for field in REVIEW_FIELDS}
        metadata = {"study": "common-brief-trial", "trial_review": review, "spoken_semantics": brief["spoken_semantics"], "visual_purpose": brief["visual_purpose"]}
        final_state = len(visual_case["scene_states"]) - 1 if brief["route"] == "approved_still" else 0
        assets.append(_render_asset(output, visual_case, brief["track"], brief["route"], approved_state_index=final_state, asset_id=brief["id"], manifest_case_id=brief["id"], metadata=metadata))
    abstentions = [{"id": brief["id"], "title": brief["title"], "reason": brief["reason"], "trial_review": {field: brief[field] for field in REVIEW_FIELDS}} for brief in briefs if not brief["candidate"]]
    result = {"renderer": "ffmpeg local no-key deterministic", "study": "common-brief-trial", "assets": assets, "briefs": briefs, "abstentions": abstentions}
    (output / "render-manifest.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result
