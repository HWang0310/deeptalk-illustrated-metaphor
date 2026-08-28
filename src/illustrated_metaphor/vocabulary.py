"""Original, inspectable visual vocabulary for the B1 metaphor-system study."""

from dataclasses import dataclass


@dataclass(frozen=True)
class MetaphorSpec:
    """One cognitive claim expressed through a bounded physical scene grammar."""

    case_id: str
    metaphor: str
    actor_role: str | None
    objects: tuple[str, ...]
    relation: str
    focal_object: str
    state_change: str
    annotation_position: str
    motion_opportunity: str


CASE_IDS = (
    "burden-growth",
    "tug-of-war",
    "speed-loop",
    "hidden-fragility",
    "information-overload",
    "network-effect",
    "state-transition",
)


SPECS = {
    "burden-growth": MetaphorSpec("burden-growth", "burden", "bearer", ("load", "path"), "actor braces against an expanding load", "load", "load grows and lowers", "upper-left", "load emphasis"),
    "tug-of-war": MetaphorSpec("tug-of-war", "tension", "counter-force", ("rope", "resource-block"), "opposing force blocks displace a shared rope", "rope-midpoint", "tension pulls away from balance", "upper-left", "tension pulse"),
    "speed-loop": MetaphorSpec("speed-loop", "loop", "runner", ("wheel", "path"), "actor is drawn beside a self-reinforcing wheel", "wheel", "wheel expands and arrow advances", "upper-left", "rotational focal push"),
    "hidden-fragility": MetaphorSpec("hidden-fragility", "fragility", "observer", ("bridge", "crack"), "a calm bridge spans a newly visible crack", "crack", "concealed crack opens below bridge", "upper-left", "crack reveal"),
    "information-overload": MetaphorSpec("information-overload", "overload", "receiver", ("signal-card", "container", "stack"), "signal cards overflow a bounded container", "container-mouth", "cards accumulate past container capacity", "upper-left", "staged card reveal"),
    "network-effect": MetaphorSpec("network-effect", "network", None, ("network-node", "path", "signal-card"), "one origin node activates linked nodes", "origin-node", "linked nodes receive activation", "upper-left", "propagation cut"),
    "state-transition": MetaphorSpec("state-transition", "transition", "chooser", ("gate", "threshold", "path"), "actor crosses a threshold through an open gate", "gate", "path changes from reactive to active", "upper-left", "gate and path reveal"),
}


def get_metaphor_spec(case_id: str) -> MetaphorSpec:
    """Return the one approved V0.2 grammar for a benchmark case."""
    try:
        return SPECS[case_id]
    except KeyError as error:
        raise ValueError(f"unknown V0.2 metaphor case: {case_id}") from error


def _actor(x: int, y: int, lean: int = 0, direction: int = 1) -> str:
    arm_end = x + direction * (72 + lean)
    return f'''<g class="generic-paper-actor" data-role="actor"><circle cx="{x}" cy="{y - 112}" r="31" fill="#f06f4b"/><path d="M{x - 52} {y + 105} L{x - 20} {y - 70} L{x + 68} {y - 20} L{x + 36} {y + 105} Z" fill="#315f9f"/><path d="M{x + 30} {y - 25} L{arm_end} {y - 45}" stroke="#f06f4b" stroke-width="23" stroke-linecap="round"/><path d="M{x - 12} {y + 100} L{x - 48} {y + 148} M{x + 25} {y + 100} L{x + 68} {y + 145}" stroke="#27313d" stroke-width="13" stroke-linecap="round"/></g>'''


def _object(name: str, contents: str, focal: bool = False) -> str:
    focus = ' data-focal="true"' if focal else ""
    return f'<g data-role="object" data-object="{name}"{focus}>{contents}</g>'


def _burden(state: int) -> str:
    radius = 72 + state * 26
    return _actor(360, 410, state * 8) + _object("load", f'<circle cx="770" cy="425" r="{radius}" fill="#c4d85a" stroke="#27313d" stroke-width="9"/><path d="M465 420 H{688 - state * 10}" stroke="#f06f4b" stroke-width="18" stroke-linecap="round"/>', True) + _object("path", '<path d="M255 575 H1000" stroke="#27313d" stroke-width="10" stroke-linecap="round"/>')


def _tension(state: int) -> str:
    shift = state * 22
    return _actor(350 - shift, 410, 0, 1) + _actor(910 + shift, 410, 0, -1) + _object("rope", f'<path d="M440 400 C600 {375 - state * 8} 690 {430 + state * 8} 830 400" fill="none" stroke="#ef7350" stroke-width="14"/><circle cx="640" cy="{402 + state * 3}" r="17" fill="#c4d85a" stroke="#27313d" stroke-width="6"/>', True) + _object("resource-block", '<rect x="590" y="485" width="100" height="52" rx="13" fill="#315f9f" stroke="#27313d" stroke-width="7"/>')


def _loop(state: int) -> str:
    radius = 86 + state * 10
    return _actor(360, 430, state * 4) + _object("wheel", f'<circle cx="770" cy="410" r="{radius}" fill="none" stroke="#315f9f" stroke-width="20"/><path d="M{820 + state * 6} 322 L875 345 L837 387" fill="none" stroke="#f06f4b" stroke-width="16" stroke-linejoin="round"/>', True) + _object("path", '<path d="M270 575 C510 485 770 525 1010 575" fill="none" stroke="#27313d" stroke-width="10"/>')


def _fragility(state: int) -> str:
    crack = "" if state == 0 else '<path d="M755 512 L780 545 L804 510 L830 555 L860 520" fill="none" stroke="#ef7350" stroke-width="13" stroke-linejoin="round"/>'
    return _actor(370, 390) + _object("bridge", '<path d="M560 505 H950" stroke="#c4d85a" stroke-width="35" stroke-linecap="round"/><path d="M560 530 H950" stroke="#27313d" stroke-width="9" stroke-linecap="round"/>') + _object("crack", f'<path d="M755 518 H860" stroke="#27313d" stroke-width="8"/>{crack}', True)


def _overload(state: int) -> str:
    cards = "".join(f'<rect x="{560 + index * 52}" y="{298 + (index % 2) * 74 - min(state, 2) * 14}" width="76" height="104" rx="14" fill="#{("315f9f", "ef7350", "c4d85a")[index % 3]}" stroke="#27313d" stroke-width="5"/>' for index in range(2 + state * 2))
    return _actor(335, 425, state * 3) + _object("container", '<path d="M855 340 V500 Q855 530 885 530 H970 Q1000 530 1000 500 V340" fill="none" stroke="#27313d" stroke-width="12"/><path d="M842 340 H1013" stroke="#27313d" stroke-width="12" stroke-linecap="round"/>', True) + _object("signal-card", cards) + _object("stack", '<path d="M545 545 H815" stroke="#27313d" stroke-width="9" stroke-linecap="round"/>')


def _network(state: int) -> str:
    secondary_fill = "#c4d85a" if state else "#fffdf8"
    nodes = '<path d="M650 420 L790 335 M650 420 L865 420 M650 420 L790 515" stroke="#27313d" stroke-width="9" stroke-linecap="round"/>'
    nodes += '<circle cx="650" cy="420" r="38" fill="#ef7350" stroke="#27313d" stroke-width="8"/>'
    nodes += f'<circle cx="790" cy="335" r="27" fill="{secondary_fill}" stroke="#27313d" stroke-width="8"/><circle cx="865" cy="420" r="27" fill="{secondary_fill}" stroke="#27313d" stroke-width="8"/><circle cx="790" cy="515" r="27" fill="{secondary_fill}" stroke="#27313d" stroke-width="8"/>'
    return _object("network-node", nodes, True) + _object("path", '<path d="M475 575 H975" stroke="#27313d" stroke-width="10" stroke-linecap="round"/>') + _object("signal-card", f'<rect x="{520 + state * 40}" y="375" width="68" height="60" rx="13" fill="#315f9f" stroke="#27313d" stroke-width="6"/>')


def _transition(state: int) -> str:
    x = 360 + state * 115
    return _actor(x, 420, state * 4) + _object("gate", '<path d="M750 520 V320 H900 V520" fill="none" stroke="#27313d" stroke-width="13"/><path d="M825 320 V520" stroke="#c4d85a" stroke-width="20"/>', True) + _object("threshold", '<path d="M650 535 H970" stroke="#ef7350" stroke-width="15" stroke-linecap="round"/>') + _object("path", f'<path d="M250 575 C490 530 {590 + state * 25} 540 750 535" fill="none" stroke="#315f9f" stroke-width="16" stroke-linecap="round"/>')


RENDERERS = {
    "burden-growth": _burden,
    "tug-of-war": _tension,
    "speed-loop": _loop,
    "hidden-fragility": _fragility,
    "information-overload": _overload,
    "network-effect": _network,
    "state-transition": _transition,
}


def render_b1_system(case_id: str, state_index: int) -> str:
    """Render original B1 components, with inspectable role and focal metadata."""
    spec = get_metaphor_spec(case_id)
    state = max(0, min(state_index, 2))
    body = RENDERERS[case_id](state)
    actor = spec.actor_role or "object-only"
    return f'<g class="b1-metaphor-system" data-metaphor="{spec.metaphor}" data-focal-object="{spec.focal_object}" data-actor-role="{actor}" data-relation="{spec.relation}">{body}</g>'
