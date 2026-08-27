"""Deterministic route plans. Rendering is deliberately separate from planning."""

from pathlib import Path


ROUTES = {"approved_still", "structured_hybrid", "independent_keyframes"}


def build_route(route: str, case: dict, output: Path) -> dict:
    """Build a declarative, ordered plan for one motion route."""
    if route not in ROUTES:
        raise ValueError(f"unknown route: {route}")
    state_names = [state["name"] for state in case["scene_states"]]
    if route == "approved_still":
        frame_plan = [{"state": state_names[0], "motion": "reveal-pan-emphasis"}, {"state": state_names[-1], "motion": "cut-hold"}]
    elif route == "structured_hybrid":
        frame_plan = [{"state": name, "motion": "state-cut"} for name in state_names]
    else:
        frame_plan = [{"state": name, "motion": "independent-keyframe"} for name in state_names]
    return {"route": route, "case_id": case["id"], "duration_seconds": case["duration_seconds"], "state_names": state_names, "frame_plan": frame_plan, "output_dir": str(output)}
