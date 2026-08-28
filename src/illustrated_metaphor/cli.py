"""Prototype runner; intentionally a natural internal tool rather than a final plugin API."""

import hashlib
import json
from pathlib import Path

from .benchmark import load_cases
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


def _render_asset(output: Path, case: dict, track: str, route: str) -> dict:
    plan = build_route(route, case, output)
    state_indexes = [0] if route == "approved_still" else list(range(len(case["scene_states"])))
    frame_dir = output / case["id"] / track / route / "sequence"
    for number, state_index in enumerate(state_indexes, 1):
        render_frame(track, case["text"], state_index, frame_dir / f"frame_{number:03d}.png", case_id=case["id"])
    mp4_path = frame_dir.parent / "asset.mp4"
    pattern = str(frame_dir / "frame_%03d.png")
    assemble_mp4(pattern, len(state_indexes), case["duration_seconds"], mp4_path, single_still=plan["source_mode"] == "single_approved_still")
    contact_path = frame_dir.parent / "contact-sheet.png"
    contact_sheet(pattern, len(state_indexes), contact_path)
    files = [str(mp4_path), str(contact_path)] + [str(path) for path in sorted(frame_dir.glob("*.png"))]
    asset = {**plan, "track": track, "provenance": TRACK_PROVENANCE[track], "files": files}
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
            assets.append(_render_asset(output, case, track, "approved_still"))
        if case["id"] in selective_state_cases:
            assets.append(_render_asset(output, case, "b1_metaphor_system", "structured_hybrid"))
    result = {"renderer": "ffmpeg local no-key deterministic", "study": "v0.2-original-metaphor-system", "assets": assets}
    (output / "render-manifest.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result
