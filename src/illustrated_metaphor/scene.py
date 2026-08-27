"""Scene-state validation shared by render routes."""


def validate_scene(scene: dict) -> list[str]:
    """Return human-readable violations without mutating the scene."""
    errors = []
    duration = scene.get("duration_seconds")
    if not isinstance(duration, (int, float)) or not 3 <= duration <= 10:
        errors.append("duration_seconds must be between 3 and 10")
    states = scene.get("scene_states")
    if not isinstance(states, list) or not states:
        errors.append("scene_states must contain at least one state")
    else:
        for index, state in enumerate(states):
            if not isinstance(state, dict) or not str(state.get("name", "")).strip():
                errors.append(f"scene_states[{index}].name is required")
    return errors
