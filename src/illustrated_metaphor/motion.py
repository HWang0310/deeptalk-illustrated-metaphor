"""Deterministic route plans. Rendering is deliberately separate from planning."""

from pathlib import Path

from .vocabulary import get_metaphor_spec


ROUTES = {"approved_still", "structured_hybrid", "independent_keyframes"}


def build_route(route: str, case: dict, output: Path) -> dict:
    """Build a declarative, ordered plan for one motion route."""
    if route not in ROUTES:
        raise ValueError(f"unknown route: {route}")
    state_names = [state["name"] for state in case["scene_states"]]
    focal_object = get_metaphor_spec(case["id"]).focal_object
    if route == "approved_still":
        frame_plan = [{"state": state_names[0], "motion": "reveal-pan-emphasis"}, {"state": state_names[-1], "motion": "cut-hold"}]
        motion_beats = [
            {"motion": "reveal", "seconds": 0.35},
            {"motion": "focal_push", "seconds": 1.65},
            {"motion": "hold", "seconds": case["duration_seconds"] - 2.0},
        ]
    elif route == "structured_hybrid":
        frame_plan = [{"state": name, "motion": "state-cut"} for name in state_names]
        motion_beats = [{"motion": "state_hold", "seconds": case["duration_seconds"] / len(state_names)} for _ in state_names]
    else:
        frame_plan = [{"state": name, "motion": "independent-keyframe"} for name in state_names]
        motion_beats = [{"motion": "keyframe_hold", "seconds": case["duration_seconds"] / len(state_names)} for _ in state_names]
    source_mode = "single_approved_still" if route == "approved_still" else "ordered_scene_states"
    return {"route": route, "case_id": case["id"], "duration_seconds": case["duration_seconds"], "state_names": state_names, "frame_plan": frame_plan, "motion_beats": motion_beats, "source_mode": source_mode, "focal_object": focal_object, "focal_treatment": "focal push is a whole-frame camera move; no component animation claimed", "output_dir": str(output)}
