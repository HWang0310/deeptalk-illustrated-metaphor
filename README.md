# DeepTalk Illustrated Metaphor

A standalone R&D project for turning a cognitive point, metaphor, or state change into a 3–10 second illustrated motion asset suitable for editorial talking-head video.

V0 studies two deliberately separate prototype tracks:

- **Track A — Xiaohei-inspired Reference Prototype:** audits and tests the observed upstream visual method, with explicit provenance and no claim of ownership over Xiaohei / 小黑.
- **Track B — Neutral / Original Illustrated Metaphor Prototype:** tests whether the underlying method works without the upstream identity, using an original neutral collage language.

The reliable V0 baseline is **approved still → deterministic motion assembly**. Structured scene-state hybrid is the stop-motion exploration path; independent keyframes are a high-risk comparator.

## Quick start

```bash
python3 -m unittest discover -s tests -v
python3 scripts/render_prototypes.py --output output/v0
python3 scripts/render_prototypes.py --v02-comparison --output output/v0.2/comparison
python3 scripts/render_prototypes.py --common-brief-trial --output output/common-brief-trial
```

Generated MP4s, PNG/SVG sequences, manifests, and contact sheets are intentionally local under `output/`.

Read [docs/INDEX.md](docs/INDEX.md) for the research record and [PROJECT_STATE.md](PROJECT_STATE.md) for current truth.

The project is MIT-licensed. Its Track A research boundary and upstream attribution are documented in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
