"""Track-specific SVG stills used as inspectable research artifacts."""

from html import escape


def render_svg(case: dict, track: str, state_index: int) -> str:
    """Render an intentionally simple 16:9 cognitive-metaphor still as SVG."""
    text = escape(str(case.get("text", "")))
    scale = 1 + state_index * 0.35
    if track == "a_reference":
        body = f'''<g class="black-figure"><circle cx="365" cy="295" r="34" fill="#171717"/><path d="M365 329 L365 440 M365 360 L310 405 M365 360 L425 385 M365 440 L325 505 M365 440 L410 505" stroke="#171717" stroke-width="26" stroke-linecap="round"/></g><circle cx="{690 + state_index * 45}" cy="430" r="{100 * scale:.0f}" fill="#f2c94c"/><path d="M430 450 L{610 + state_index * 35} 450" stroke="#171717" stroke-width="10" stroke-linecap="round"/>'''
        provenance = 'data-provenance="upstream-reference-only"'
    elif track == "b_neutral":
        body = f'''<g class="paper-collage"><path class="neutral-form" d="M315 500 L355 300 L420 345 L450 505 Z" fill="#3766a8"/><circle class="neutral-form" cx="385" cy="258" r="42" fill="#f37b4b"/><path d="M280 450 L500 400" stroke="#f37b4b" stroke-width="16" stroke-linecap="round"/></g><path d="M{620 + state_index * 25} 485 L{735 + state_index * 25} 300 L850 485 Z" fill="#eadbc8" stroke="#2d2c36" stroke-width="8"/><circle cx="735" cy="420" r="{72 * scale:.0f}" fill="#c7d85b"/>'''
        provenance = 'data-provenance="original-neutral-prototype"'
    else:
        raise ValueError(f"unknown track: {track}")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720" data-track="{track}" {provenance}><rect width="1280" height="720" fill="#fbf8f2"/><rect x="70" y="80" width="1140" height="560" rx="30" fill="#fffdf8" stroke="#2d2c36" stroke-width="7"/>{body}<text x="100" y="150" font-family="PingFang SC, PingFang, sans-serif" font-size="42" font-weight="600" fill="#2d2c36">{text}</text><text x="100" y="595" font-family="PingFang SC, PingFang, sans-serif" font-size="20" fill="#706c65">{escape(case.get('id', 'scene'))} · state {state_index + 1}</text></svg>'''
