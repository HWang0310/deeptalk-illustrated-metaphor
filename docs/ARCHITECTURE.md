# Architecture

The local V0 pipeline is:

`benchmark case → scene-state validation → track-specific deterministic SVG stills → route-specific frame plan → FFmpeg MP4 assembly → manifests/contact sheet → QA report`.

The natural input is a small cognitive-metaphor brief (intent, scene states, sparse copy, duration, and checks). The natural output is an asset package: MP4, a still/sequence, contact sheet, provenance and render metadata, and QA evidence. This is deliberately not a final DeepTalk plugin contract.

The repository has a minimal validated Codex plugin manifest, but exposes no final Core integration surface. V0's real input fields are `semantic_intent`, `metaphor`, `scene_states`, `text`, `duration_seconds`, and `qa_criteria`; its output is local asset evidence plus a manifest rather than a published episode asset.

V0.1 adds case-specific metaphor grammar between scene validation and SVG generation. For approved-still output it renders one approved SVG/PNG then applies local FFmpeg fade-in and bounded focal-push assembly. Structured-state output continues to render ordered explicit scene states. This keeps deterministic typography and motion distinct from optional model still research.

## V0.2 original metaphor system

V0.2 inserts a small declarative vocabulary layer between the benchmark and B1 SVG renderer:

`benchmark case → MetaphorSpec → original cut-paper actor/object components → SVG → sips PNG → FFmpeg MP4 → manifest + structural QA`.

`src/illustrated_metaphor/vocabulary.py` is intentionally not a general scene graph. Its seven immutable `MetaphorSpec` values express actor role (or object-only), 1–4 original objects, a spatial relation, focal object, state change, annotation placement, and a truthful motion opportunity. The B1 V0.2 track consumes this layer; Track A, V0.1 B1, and B2 are preserved comparison renderers.

For V0.2 approved-still evidence, the one source SVG is the final readable declared scene state, then local FFmpeg applies a 0.35-second fade, a bounded 3.5% whole-frame focal push, and hold. The focal target is metadata for composition review; it is not a claim of independently animated SVG components. Structured states are only emitted for burden growth, information overload, and state transition.
