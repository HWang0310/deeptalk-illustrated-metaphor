# DeepTalk Illustrated Metaphor

An independent visual plugin for turning a cognitive point, metaphor, state change, or editorial idea into a short illustrated motion asset for DeepTalk-style talking-head video.

The project keeps two deliberately separate historical research tracks:

- **Track A — Xiaohei-inspired Reference Prototype:** upstream-reference research with explicit provenance and no ownership claim over Xiaohei / 小黑.
- **Track B — Neutral / Original Illustrated Metaphor Prototype:** the independent neutral/original implementation path used to test the underlying visual method without upstream identity.

The reliable rendering baseline is approved still → deterministic motion assembly. Structured scene-state hybrid is the controlled motion path; independent keyframes remain a higher-risk comparator.

## Current Accepted Runtime

- Canonical identity: **Illustrated Metaphor**
- Contract: `visual-asset-plugin-contract/1`
- Runtime behavior baseline: `48848affe018fc2cff8ee15bad7a09bb002776e4`
- Canonical runner: `python3 scripts/contract_runner.py`
- Status: `ACCEPTED / IMPLEMENTED_UNRELEASED`
- DeepTalk compatibility reference: `HWang0310/deep-talk-studio` accepted Phase 5 baseline `db172cecc60ca6b0c276ec42010b113a767bc7b3`

Repository governance rule: `main` represents the latest plugin-local accepted stable runtime. New optimization work starts from `main` on an isolated task branch. Plugin-local acceptance does **not** authorize DeepTalk Core to repin automatically; DeepTalk Nexus performs a separate integration review.

See [docs/DEEPTALK-INTEGRATION.md](docs/DEEPTALK-INTEGRATION.md) before any visual-quality or runtime change.

## Current quality direction

Real-A-roll owner-visible evidence shows a recognizable, clean visual family and valid creator-visible media, while also exposing the next quality problem: semantic specificity. Different opportunities can collapse into generic metaphor patterns, and mechanism-heavy ideas may be represented too abstractly to add enough explanatory value.

The next optimization track should therefore prioritize opportunity-specific metaphor/action/composition mapping, broader project-owned visual vocabulary, stronger semantic anchors, and honest abstention when a metaphor would reduce precision.

## Quick start

```bash
python3 -m unittest discover -s tests -v
python3 scripts/render_prototypes.py --output output/v0
python3 scripts/render_prototypes.py --v02-comparison --output output/v0.2/comparison
python3 scripts/render_prototypes.py --common-brief-trial --output output/common-brief-trial
python3 scripts/contract_runner.py --version
```

Generated MP4s, PNG/SVG sequences, manifests, and contact sheets are intentionally local under `output/` unless a reviewed task explicitly versions a small non-private evidence artifact.

Read [PROJECT_STATE.md](PROJECT_STATE.md), [docs/INDEX.md](docs/INDEX.md), and [docs/DEEPTALK-INTEGRATION.md](docs/DEEPTALK-INTEGRATION.md) for current project truth and integration boundaries.

The project is MIT-licensed. Track A provenance and upstream attribution remain documented in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
