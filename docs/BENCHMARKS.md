# Benchmarks

V0 uses seven non-private generic cognitive-metaphor tasks: burden growth, tug of war, speed loop, hidden fragility, information overload, network effect, and state transition. Every case specifies semantic intent, physical metaphor, ordered states, one sparse Chinese label, 4–5 second duration, and QA criteria. The same intent runs through both tracks and all three motion routes.

The executable definition is [`benchmarks/v0-cases.json`](../benchmarks/v0-cases.json). This yields 42 deterministic route assets (7 cases × 2 tracks × 3 routes).

V0.1 keeps these exact seven cases. Its final comparable corpus contains 35 assets: Track A approved-still reference; Track B V0 neutral control; B1 Paper Relay approved-still and structured-state; and B2 Object Theatre approved-still. Each case maps to a distinct physical grammar rather than differing only by its label.

## V0.2 comparison

V0.2 keeps the exact same seven semantic cases. Its 31-asset corpus contains four approved-still comparators for every case—Track A frozen reference, B1 V0.1 Paper Relay, B1 V0.2 Original Metaphor System, and B2 Object Theatre—plus V0.2 B1 structured-state evidence only for burden growth, information overload, and state transition.

The V0.2 B1 mappings are burden/load, tension/rope, loop/wheel, fragility/bridge-and-crack, overload/container-and-signals, network/origin-node, and transition/gate-threshold-barrier. They use the first composable original vocabulary: load, barrier, bridge, container, stack, rope, wheel, threshold, crack, network node, path, gate, resource block, and signal card. These are original SVG primitives; no Xiaohei asset or upstream source is imported.

## Common Brief Trial

The Common Brief Trial uses [`benchmarks/common-briefs.json`](../benchmarks/common-briefs.json), a separate fixed set of CB01–CB08 supplied by Product Review. It does not replace the V0 seven-case benchmark. The trial records suitability and permits `SUITABLE`, `BORDERLINE`, and `ABSTAIN`; CB08 numeric evidence is intentionally an abstention. No other plugin trial result was read to influence the assessment.
