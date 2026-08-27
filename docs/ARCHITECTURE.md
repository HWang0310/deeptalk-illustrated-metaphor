# Architecture

The local V0 pipeline is:

`benchmark case → scene-state validation → track-specific deterministic SVG stills → route-specific frame plan → FFmpeg MP4 assembly → manifests/contact sheet → QA report`.

The natural input is a small cognitive-metaphor brief (intent, scene states, sparse copy, duration, and checks). The natural output is an asset package: MP4, a still/sequence, contact sheet, provenance and render metadata, and QA evidence. This is deliberately not a final DeepTalk plugin contract.

The repository has a minimal validated Codex plugin manifest, but exposes no final Core integration surface. V0's real input fields are `semantic_intent`, `metaphor`, `scene_states`, `text`, `duration_seconds`, and `qa_criteria`; its output is local asset evidence plus a manifest rather than a published episode asset.
