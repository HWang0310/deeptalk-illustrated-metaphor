"""Prototype runner; intentionally a natural internal tool rather than a final plugin API."""

import hashlib
import json
from pathlib import Path

from .benchmark import load_cases
from .motion import build_route
from .qa import run_qa
from .render import assemble_mp4, contact_sheet, render_frame


def render_prototypes(output: Path, case_limit: int | None = None) -> dict:
    """Render both tracks across all comparison routes and write evidence metadata."""
    output.mkdir(parents=True, exist_ok=True)
    assets = []
    for case in load_cases("benchmarks/v0-cases.json")[:case_limit]:
        for track in case["tracks"]:
            for route in ("approved_still", "structured_hybrid", "independent_keyframes"):
                plan = build_route(route, case, output)
                state_indexes = [0, len(case["scene_states"]) - 1] if route == "approved_still" else list(range(len(case["scene_states"])))
                frame_dir = output / case["id"] / track / route / "sequence"
                for number, state_index in enumerate(state_indexes, 1):
                    render_frame(track, case["text"], state_index, frame_dir / f"frame_{number:03d}.png")
                mp4_path = frame_dir.parent / "asset.mp4"
                pattern = str(frame_dir / "frame_%03d.png")
                assemble_mp4(pattern, len(state_indexes), case["duration_seconds"], mp4_path)
                contact_path = frame_dir.parent / "contact-sheet.png"
                contact_sheet(pattern, len(state_indexes), contact_path)
                files = [str(mp4_path), str(contact_path)] + [str(path) for path in sorted(frame_dir.glob("*.png"))]
                asset = {**plan, "track": track, "provenance": "upstream-reference-only" if track == "a_reference" else "original-neutral-prototype", "files": files}
                asset["sequence_sha256"] = hashlib.sha256(b"".join(Path(item).read_bytes() for item in files[2:])).hexdigest()
                asset["qa"] = run_qa(asset)
                (frame_dir.parent / "manifest.json").write_text(json.dumps(asset, ensure_ascii=False, indent=2), encoding="utf-8")
                assets.append(asset)
    result = {"renderer": "ffmpeg local no-key deterministic", "assets": assets}
    (output / "render-manifest.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result
