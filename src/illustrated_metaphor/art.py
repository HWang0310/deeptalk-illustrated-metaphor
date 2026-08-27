"""Track-specific SVG stills used as inspectable research artifacts."""

from html import escape


def _metaphor_overlay(case_id: str, state_index: int) -> str:
    """Return a compact, case-specific physical metaphor grammar."""
    step = state_index + 1
    if case_id == "burden-growth":
        return f'<g data-metaphor="burden"><circle cx="790" cy="425" r="{55 + step * 28}" fill="#c4d85a" stroke="#27313d" stroke-width="8"/></g>'
    if case_id == "tug-of-war":
        return f'<g data-metaphor="tension"><path d="M500 430 H920" stroke="#ef7350" stroke-width="12"/><rect x="{535 - step * 12}" y="395" width="58" height="70" fill="#315f9f"/><rect x="{835 + step * 12}" y="395" width="58" height="70" fill="#c4d85a"/></g>'
    if case_id == "speed-loop":
        return f'<g data-metaphor="loop"><circle cx="770" cy="420" r="{70 + step * 12}" fill="none" stroke="#315f9f" stroke-width="18"/><path d="M820 340 L865 355 L838 390" fill="none" stroke="#ef7350" stroke-width="15" stroke-linejoin="round"/></g>'
    if case_id == "hidden-fragility":
        return '<g data-metaphor="fragility"><path d="M610 470 H900" stroke="#27313d" stroke-width="18"/><path d="M755 470 L780 495 L805 465 L835 500" fill="none" stroke="#ef7350" stroke-width="12"/></g>'
    if case_id == "information-overload":
        cards = ''.join(f'<rect x="{620 + index * 42}" y="{330 + (index % 2) * 60}" width="70" height="90" rx="10" fill="#{color}"/>' for index, color in enumerate(("315f9f", "ef7350", "c4d85a", "315f9f", "ef7350")[: step + 2]))
        return f'<g data-metaphor="overload">{cards}<rect x="895" y="365" width="80" height="70" rx="16" fill="none" stroke="#27313d" stroke-width="10"/></g>'
    if case_id == "network-effect":
        return '<g data-metaphor="network"><path d="M705 420 L790 345 M705 420 L815 435 M705 420 L785 505" stroke="#27313d" stroke-width="9"/><circle cx="705" cy="420" r="32" fill="#ef7350"/><circle cx="790" cy="345" r="24" fill="#315f9f"/><circle cx="815" cy="435" r="24" fill="#c4d85a"/><circle cx="785" cy="505" r="24" fill="#315f9f"/></g>'
    if case_id == "state-transition":
        return f'<g data-metaphor="transition"><path d="M640 500 V340 H760 V500" fill="none" stroke="#27313d" stroke-width="12"/><path d="M590 425 H{725 + step * 28}" stroke="#ef7350" stroke-width="15"/><path d="M{705 + step * 28} 395 L{735 + step * 28} 425 L{705 + step * 28} 455" fill="none" stroke="#ef7350" stroke-width="15"/></g>'
    return '<g data-metaphor="generic"></g>'


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
    elif track == "b_paper_relay":
        body = f'''<g class="paper-relay"><path class="generic-paper-actor" d="M285 510 L340 315 L455 375 L440 510 Z" fill="#315f9f"/><circle class="generic-paper-actor" cx="385" cy="263" r="35" fill="#f06f4b"/><path class="generic-paper-actor" d="M430 392 L{575 + state_index * 20} 370" stroke="#f06f4b" stroke-width="24" stroke-linecap="round"/><path d="M270 525 H520" stroke="#27313d" stroke-width="8" stroke-linecap="round"/></g>'''
        provenance = 'data-provenance="original-language-hypothesis"'
    elif track == "b_object_theatre":
        body = f'''<g class="object-theatre"><path d="M280 500 L280 390 L510 390 L510 500" fill="none" stroke="#27313d" stroke-width="12"/><rect x="{350 + state_index * 10}" y="{330 - state_index * 12}" width="{130 + state_index * 45}" height="{110 + state_index * 38}" rx="22" fill="#ef7350"/><path d="M580 495 C650 400 {710 - state_index * 20} 390 {805 - state_index * 10} 495" fill="#f3c64e" stroke="#27313d" stroke-width="9"/><circle cx="750" cy="400" r="{38 * scale:.0f}" fill="#385f9f"/><path d="M260 535 H920" stroke="#27313d" stroke-width="12" stroke-linecap="round"/></g>'''
        provenance = 'data-provenance="original-language-hypothesis"'
    else:
        raise ValueError(f"unknown track: {track}")
    overlay = _metaphor_overlay(str(case.get("id", "")), state_index)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720" data-track="{track}" {provenance}><rect width="1280" height="720" fill="#fbf8f2"/><rect x="70" y="80" width="1140" height="560" rx="30" fill="#fffdf8" stroke="#2d2c36" stroke-width="7"/>{body}{overlay}<text x="100" y="150" font-family="PingFang SC, PingFang, sans-serif" font-size="42" font-weight="600" fill="#2d2c36">{text}</text><text x="100" y="595" font-family="PingFang SC, PingFang, sans-serif" font-size="20" fill="#706c65">{escape(case.get('id', 'scene'))} · state {state_index + 1}</text></svg>'''
