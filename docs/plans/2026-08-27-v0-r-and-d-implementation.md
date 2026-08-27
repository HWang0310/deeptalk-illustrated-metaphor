# Illustrated Metaphor V0 R&D Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a standalone, reproducible dual-track R&D prototype that turns approved illustrated metaphor stills or structured scene states into locally rendered motion assets with evidence-based QA.

**Architecture:** Python defines benchmark cases, validates scene metadata, renders deterministic SVG/PNG frames, assembles MP4 assets through FFmpeg, and produces contact sheets and QA reports. Track A is explicitly an upstream-reference research track; Track B uses a separate original neutral collage language. Both share inputs, metrics, and renderer interfaces without claiming a final DeepTalk contract.

**Tech Stack:** Python 3 standard library, SVG, FFmpeg, unittest, Git/GitHub CLI.

**Spec:** Product Review direction recorded in `PROJECT_STATE.md`; no DeepTalk Core integration or modification.

## Global Constraints

- Canonical project identity is `Illustrated Metaphor`; Xiaohei is only an upstream reference/prototype track.
- Keep generated MP4, PNG sequences, and contact sheets local and gitignored.
- Do not require an API key; make image-generation limits explicit.
- Run each behavior test red before implementation, then green before committing.
- Do not modify `/Users/hwang/Movies/Codex工作空间/deep-talk-studio`.

---

### Task 1: Repository and project memory

**Files:**
- Create: `AGENTS.md`, `README.md`, `PROJECT_STATE.md`, `ROADMAP.md`, `CHANGELOG.md`, `HANDOFF.md`
- Create: `docs/INDEX.md`, `docs/ARCHITECTURE.md`, `docs/RESEARCH.md`, `docs/BENCHMARKS.md`, `docs/QUALITY.md`

- [ ] Define standalone scope, provenance guardrails, current truth, and fresh-agent bootstrap.
- [ ] Initialize Git on `main`, configure non-sensitive local identity, and create the public GitHub repository if absent.
- [ ] Verify project status and GitHub remote.

### Task 2: Upstream audit and licensing boundary

**Files:**
- Create: `vendor/upstream-audit/ian-xiaohei-illustrations/` (gitignored clone)
- Create: `docs/plans/2026-08-27-xiaohei-upstream-audit.md`
- Create: `THIRD_PARTY_NOTICES.md`

- [ ] Clone the upstream at its observed HEAD and record exact SHA.
- [ ] Inspect README, SKILL, visual/style/IP/composition/prompt/QA/example files, LICENSE, NOTICE, and generation implementation.
- [ ] Separate observed facts from proposals; preserve required notices without copying upstream software into this project.

### Task 3: Benchmark domain and scene-state validation

**Files:**
- Create: `src/illustrated_metaphor/benchmark.py`, `src/illustrated_metaphor/scene.py`
- Create: `benchmarks/v0-cases.json`
- Create: `tests/test_benchmark.py`, `tests/test_scene.py`

**Interfaces:**
- Produces `load_cases(path: str) -> list[dict]` and `validate_scene(scene: dict) -> list[str]`.
- Consumes JSON benchmark cases with semantic intent, metaphor, states, text, duration, and QA criteria.

- [ ] Write a failing test that benchmark cases are unique, include both tracks, and contain required fields.
- [ ] Run `python3 -m unittest tests.test_benchmark -v`; expect failure because module is absent.
- [ ] Implement minimal loading and field validation; re-run test green.
- [ ] Write a failing test for scene-state rejection of missing state names or invalid duration.
- [ ] Run `python3 -m unittest tests.test_scene -v`; expect failure because validator is absent.
- [ ] Implement validator and re-run green.

### Task 4: Deterministic render and three motion routes

**Files:**
- Create: `src/illustrated_metaphor/art.py`, `src/illustrated_metaphor/render.py`, `src/illustrated_metaphor/motion.py`
- Create: `tests/test_art.py`, `tests/test_motion.py`

**Interfaces:**
- Produces `render_svg(case: dict, track: str, state_index: int) -> str`, `build_route(route: str, case: dict, output: Path) -> dict`.
- Consumes validated benchmark cases and creates transparent/local SVG frames and MP4 output via FFmpeg.

- [ ] Write a failing test asserting Track A and Track B SVG output contain distinct visual language markers and escaped Chinese annotation.
- [ ] Run `python3 -m unittest tests.test_art -v`; expect failure because renderer is absent.
- [ ] Implement deterministic SVG scene generation, including a reference-only black figure for Track A and a distinct neutral paper/collage system for Track B; run green.
- [ ] Write a failing test asserting all three route names create a manifest with duration and ordered frame states.
- [ ] Run `python3 -m unittest tests.test_motion -v`; expect failure because motion builder is absent.
- [ ] Implement approved-still deterministic assembly baseline, structured-state hybrid, and independent-keyframe comparator; run green.

### Task 5: Asset QA and reproducible prototype runner

**Files:**
- Create: `src/illustrated_metaphor/qa.py`, `src/illustrated_metaphor/cli.py`, `scripts/render_prototypes.py`
- Create: `tests/test_qa.py`, `tests/test_cli.py`

**Interfaces:**
- Produces `run_qa(asset_manifest: dict) -> dict` and CLI command `python3 scripts/render_prototypes.py --output <dir>`.
- Consumes route manifests and validates provenance, Chinese-text policy, composition, state continuity, duration, output files, repeatability hashes, and no-key status.

- [ ] Write a failing test for a QA failure when a Track A asset lacks an upstream-reference provenance note.
- [ ] Run `python3 -m unittest tests.test_qa -v`; expect failure because QA is absent.
- [ ] Implement QA checks and re-run green.
- [ ] Write a failing CLI test with a temporary output path.
- [ ] Run `python3 -m unittest tests.test_cli -v`; expect failure because CLI is absent.
- [ ] Implement CLI, run green, then render selected benchmark assets and contact sheets.

### Task 6: Evidence, documentation, commit, and publication

**Files:**
- Modify: project memory and documentation files
- Create: `docs/BENCHMARKS.md`, `docs/QUALITY.md`, `docs/RESEARCH.md`, `docs/ARCHITECTURE.md`, `HANDOFF.md`

- [ ] Record measured route outputs, QA results, Chinese/consistency observations, no-key constraints, and route recommendation.
- [ ] Run all tests, one full deterministic render, clean-tree status, and GitHub remote verification.
- [ ] Commit all source and documentation, push `main`, then update `PROJECT_STATE.md` to exact post-push truth in a final commit if needed.
