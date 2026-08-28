# Cross-Plugin Common Brief Trial Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Execute inline task-by-task with TDD; do not inspect other plugin repositories or outputs.

**Goal:** Render and document the Illustrated Metaphor response to the fixed eight-item Common Brief set, including a deliberate numeric-evidence abstention.

**Architecture:** A JSON trial definition maps each actual brief to an existing V0.2 B1 visual grammar without modifying the grammar itself. The CLI preserves both the Common Brief identity and the source visual-case identity, emits seven deterministic assets, and records review/QA metadata.

**Tech Stack:** Python standard library, JSON, SVG, macOS `sips`, FFmpeg, unittest.

**Spec:** `docs/plans/2026-08-28-common-brief-trial-design.md`

## Global Constraints

- This is an Illustrated Metaphor-only comparison experiment, not a Plugin Contract or V0.3.
- Do not read MG or Hand-drawn trial repositories, assets, or results.
- Track A remains frozen; no Common Brief Track A assets.
- B1 is primary; B2 only if clearly more natural, which is not established for this set.
- Keep Chinese deterministic and never claim model-rendered Chinese.
- Do not create a mascot, fixed character, new brand identity, or model-keyframe pipeline.
- DeepTalk Core remains unmodified.

---

### Task 1: Fixed brief definitions and loader

**Files:**
- Create: `benchmarks/common-briefs.json`
- Create: `src/illustrated_metaphor/common_briefs.py`
- Create: `tests/test_common_briefs.py`

**Interfaces:**
- Produces: `load_common_briefs(path: str = "benchmarks/common-briefs.json") -> list[dict]`.
- Consumes: exact CB01–CB08 supplied semantic briefs.

- [ ] Write a failing test asserting the exact eight ordered IDs, one ABSTAIN, seven actual candidates, and no Track A track.
- [ ] Run `PYTHONPATH=src python3 -m unittest tests.test_common_briefs -v` and confirm failure because the loader does not exist.
- [ ] Add validated JSON definitions and minimal loader.
- [ ] Re-run the focused test green and commit.

### Task 2: Trial rendering identity and QA metadata

**Files:**
- Modify: `src/illustrated_metaphor/art.py`
- Modify: `src/illustrated_metaphor/render.py`
- Modify: `src/illustrated_metaphor/cli.py`
- Modify: `src/illustrated_metaphor/qa.py`
- Modify: `scripts/render_prototypes.py`
- Modify: `tests/test_cli.py`
- Modify: `tests/test_qa.py`

**Interfaces:**
- Produces: `render_common_brief_trial(output: Path) -> dict`.
- Consumes: Common Brief records and existing V0.2 benchmark visual cases.

- [ ] Write failing tests that the runner produces seven B1 assets, preserves CB IDs/output folders, records source visual case IDs, and fails QA without required trial-review metadata.
- [ ] Run focused tests and confirm expected missing-function/assertion failures.
- [ ] Add minimal optional display/output identity fields, the trial runner, and structural trial-review QA.
- [ ] Re-run focused tests green and commit.

### Task 3: Rendered evidence and research record

**Files:**
- Modify: `docs/RESEARCH.md`
- Modify: `docs/QUALITY.md`
- Modify: `docs/BENCHMARKS.md`
- Modify: `PROJECT_STATE.md`
- Modify: `HANDOFF.md`
- Modify: `CHANGELOG.md`

- [ ] Render `output/common-brief-trial/` and a repeat corpus.
- [ ] Check manifests, QA, frame hashes, durations, contact sheets, and autonomous visual review.
- [ ] Record every CB result, why CB08 abstained, family strengths/limits, and the no-other-plugin-inspection boundary.
- [ ] Run full tests and plugin validation; commit, push, and confirm clean tree.
