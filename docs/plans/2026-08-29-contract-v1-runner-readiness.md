# Visual Asset Plugin Contract V1 — Runner Readiness Plan

> **Status:** Research-only readiness audit. No production runner is implemented here. No production source is changed. No Core or other plugin is modified. No main, tag, or release is touched.

## Repository and baseline

- **Repository:** `HWang0310/deeptalk-illustrated-metaphor`
- **Baseline main SHA:** `cf1cdfe6855aa8d2902b4506184c6d6fd0c60d74`
- **Research branch:** `agent/contract-v1-runner-readiness`
- **Core contract repo (read-only):** `HWang0310/deep-talk-studio` @ `d1c990c25e44aa55ffc2789f7b00ee2374a198be`

## Purpose

Complete all engineering mine-clearing so that a future formal runner implementation session can proceed mechanically. This document answers the 17 readiness questions and records every proposed file, test, ID input, and risk.

---

## 1. Current runtime architecture

The current pipeline is:

```
benchmark case (benchmarks/v0-cases.json)
  → scene-state validation (scene.py)
  → track-specific deterministic SVG stills (art.py + vocabulary.py)
  → route-specific frame plan (motion.py)
  → sips SVG→PNG rasterization (render.py)
  → FFmpeg MP4 assembly (render.py)
  → per-asset manifest + QA report (cli.py + qa.py)
  → root render-manifest.json (cli.py)
```

Key modules:

| Module | Role |
|---|---|
| `cli.py` | Prototype runner; four render modes (V0, V0.1, V0.2, Common Brief Trial). Contains `_render_asset()` — the atomic asset production function. |
| `render.py` | SVG→PNG via `sips`, MP4 via `ffmpeg`, contact sheet via `ffmpeg tile`. |
| `art.py` | Track-specific SVG generation; delegates B1 V0.2 to `vocabulary.py`. |
| `vocabulary.py` | Seven immutable `MetaphorSpec` dataclasses; original SVG primitive renderers. |
| `motion.py` | Three route plans: `approved_still`, `structured_hybrid`, `independent_keyframes`. |
| `qa.py` | Manifest-level QA: provenance, duration, files, state continuity, V0.2 structural readability, Common Brief rubric. |
| `common_briefs.py` | Fixed CB01–CB08 loader and validator. |
| `benchmark.py` | V0 seven-case loader and validator. |
| `scene.py` | Duration and scene-state validation. |
| `scripts/render_prototypes.py` | CLI entry point with `--output`, `--v01-comparison`, `--v02-comparison`, `--common-brief-trial`. |

## 2. Current CLI/render path

The current entry point is `scripts/render_prototypes.py`, which:
1. Inserts `src/` into `sys.path`.
2. Parses `--output`, `--case-limit`, `--v01-comparison`, `--v02-comparison`, `--common-brief-trial`.
3. Calls one of four functions in `cli.py`.
4. Prints `"Rendered N assets to <output>"`.

This is explicitly labeled "Prototype runner; intentionally a natural internal tool rather than a final plugin API" in `cli.py` line 1. It renders **fixed benchmark fixtures** — it has no dynamic request/response interface.

The Core example config in `config/visual-asset-plugins.example.json` expects:
```json
{
  "plugin_id": "org.deeptalk.illustrated-metaphor",
  "argv_prefix": ["python3", "scripts/contract_runner.py"],
  "plugin_version_command": ["python3", "scripts/contract_runner.py", "--version"]
}
```

So Core expects a new `scripts/contract_runner.py` with `--request`, `--result`, `--output-dir`, and `--version` flags.

## 3. Answer to 17 readiness questions

### Q1: Current most natural runner entrypoint

**Answer:** A new file `scripts/contract_runner.py` at the repository root.

Rationale:
- Core's example config already names this exact path.
- Core's adapter (`visual_plugin_adapter.py`) calls `argv_prefix + ["--request", <path>, "--result", <path>, "--output-dir", <path>]` with `cwd = plugin_root`.
- The existing `scripts/render_prototypes.py` is the natural structural reference, but it renders fixed fixtures and lacks request/result/output-dir flags.
- The runner should import from `src/illustrated_metaphor/` (same `sys.path` insertion pattern) and reuse existing `render.py`, `art.py`, `vocabulary.py`, `motion.py`, `qa.py`, `common_briefs.py`, and `benchmark.py`.

The runner's flow:
```
--version → print plugin version string, exit 0
--request <path> --result <path> --output-dir <path>:
  1. Read and parse request JSON
  2. Route to suitability or generation based on presence of proposal_id
  3. For suitability: assess the Opportunity, return Suitability Response
  4. For generation: produce an actual asset, return Generation Result
  5. Write result JSON atomically to --result path
```

### Q2: Suitability mapping to SUITABLE/BORDERLINE/ABSTAIN

**Answer:** Map dynamically based on `opportunity.spoken_semantics` and `opportunity.visual_purpose` against the Common Brief Trial evidence.

The existing evidence is in `benchmarks/common-briefs.json` and `docs/COMMON_BRIEF_TRIAL.md`. Eight fixed briefs map to:

| Suitability | Count | CB IDs | Family capability |
|---|---|---|---|
| SUITABLE | 4 | CB03, CB04, CB05, CB06 | Physical metaphor, agency/tension, loops, surface-vs-mechanism |
| BORDERLINE | 3 | CB01, CB02, CB07 | Core judgment, causal transmission, rule change |
| ABSTAIN | 1 | CB08 | Numeric evidence |

For a dynamic Opportunity, the runner should use a keyword/pattern matcher against `spoken_semantics` and `visual_purpose`:

- **ABSTAIN** if the semantics require exact numeric evidence, precise percentages, or data comparison that would become decorative rather than evidentiary.
- **BORDERLINE** if the semantics involve dense causal chains, conditional logical judgments, or core business judgments where the metaphor conveys the transition but not its exact business condition.
- **SUITABLE** if the semantics involve accumulation/pressure, feedback loops, two-side tension, surface-vs-mechanism, physical constraints, state changes, or agency/tension.

The runner's suitability function should be a pure function of the Opportunity text fields. It must return `operation_status: COMPLETED`, `proposal_id`, `suitability`, and `reason`.

The exact keyword mapping should be derived from the Common Brief rubric fields (`semantic_clarity`, `metaphor_clarity`, `family_naturalness`, `metaphor_overreach`) and the documented family capability boundary.

### Q3: Opportunity → B1 V0.2 internal structure mapping

**Answer:** Map via a two-step translation:

1. **Opportunity → visual_case_id:** Match `spoken_semantics` and `visual_purpose` to one of the seven V0.2 benchmark cases (`burden-growth`, `tug-of-war`, `speed-loop`, `hidden-fragility`, `information-overload`, `network-effect`, `state-transition`). This match uses the `semantic_intent` and `metaphor` fields in `benchmarks/v0-cases.json` as the reference.

2. **visual_case_id → B1 V0.2 structure:** Use the existing `vocabulary.get_metaphor_spec(case_id)` to get the immutable `MetaphorSpec` (actor_role, objects, relation, focal_object, state_change, annotation_position, motion_opportunity). Then use the existing `motion.build_route(route, case, output)` to get a frame plan.

The `candidate_text` for the asset should be derived from the Opportunity's `spoken_semantics` (condensed to a short Chinese label) or from the `visual_purpose` if the semantics are too dense.

The route selection should follow the Common Brief Trial pattern:
- `approved_still` for tension, surface-vs-mechanism, and single-state concepts.
- `structured_hybrid` for accumulation, loops, and state transitions where the state change itself is the central claim.

The canvas size from the Opportunity (1920×1080) differs from the current renderer's 1280×720. The runner should either:
- Scale the SVG viewBox to the requested canvas, or
- Render at 1280×720 and note the canvas mismatch in `plugin_metadata`.

The simplest deterministic approach: keep the SVG viewBox at 1280×720 and let FFmpeg scale to the requested canvas. This preserves all existing determinism.

### Q4: Avoiding committed Common Brief fixture lookup

**Answer:** Yes, this is achievable.

The runner should NOT read `benchmarks/common-briefs.json` or `benchmarks/v0-cases.json` at runtime. Instead:

1. **Embed a pure suitability function** that pattern-matches `spoken_semantics` + `visual_purpose` text fields against documented family capabilities. This function is self-contained and does not require fixture file I/O.

2. **Embed a case-selection function** that maps the Opportunity to one of the seven metaphor patterns. This function returns a `visual_case_id` and a `route`. This is pure logic, not a fixture lookup.

3. **Construct the visual case dict in-memory** from the mapped case_id, using the hardcoded `SPECS` in `vocabulary.py` and the case structure from `benchmark.py`. The scene_states can be generic (`["start", "change", "final"]`) or derived from the MetaphorSpec's `state_change` field.

4. **Use the existing `render_frame()` and `assemble_mp4()` functions** to produce the actual asset.

This means the runner is fully self-contained: it reads only the Core-supplied request JSON and writes only to the Core-supplied output directory. No committed fixture file is needed at runtime.

### Q5: Dynamic asset generation

**Answer:** The runner can generate one actual asset by:

1. Parse the Opportunity from the generation request.
2. Map the Opportunity to a `visual_case_id` and `route` (same function as suitability).
3. Build a minimal case dict: `{"id": visual_case_id, "text": candidate_text, "scene_states": [...], "duration_seconds": target_duration_ms / 1000, "tracks": ["b1_metaphor_system"]}`.
4. Call `_render_asset(output_dir, case, "b1_metaphor_system", route, approved_state_index=<final>, asset_id=candidate_id, manifest_case_id=opportunity_id, metadata={...})`.
5. Collect the produced files: MP4, contact sheet, PNG/SVG frames, per-asset manifest.
6. Compute SHA-256 of the PRIMARY_MEDIA (MP4).
7. Build the Contract V1 Generation Result JSON with candidate, artifacts, qa, provenance.
8. Write atomically to `--result` path.

The `_render_asset()` function is already atomic per-asset: it creates a subdirectory, renders frames, assembles MP4, writes manifest, and returns the asset dict. The runner wraps this and translates to Contract V1 format.

Duration: the existing renderer derives duration from `case["duration_seconds"]`. The runner should compute this from `opportunity["target_duration_ms"]` (clamped to 3–10 seconds per existing QA constraint). The actual MP4 duration may differ slightly from the target due to FFmpeg frame quantization; the runner should report the actual `duration_ms` in the candidate.

### Q6: Minimum file changes

**Answer:** The minimum changes for a future implementation session:

| File | Change type | Responsibility |
|---|---|---|
| `scripts/contract_runner.py` | **NEW** | Contract V1 runner entry point: `--version`, `--request`, `--result`, `--output-dir`. Routes to suitability or generation. |
| `src/illustrated_metaphor/contract.py` | **NEW** | Contract V1 logic: suitability assessment function, opportunity→case mapping, generation result builder, artifact packaging. Pure functions, no I/O. |
| `src/illustrated_metaphor/__init__.py` | **MODIFY** | Add `__version__` constant for `--version` output. |
| `tests/test_contract.py` | **NEW** | Unit tests for suitability mapping, case selection, generation result shape, artifact completeness, determinism. |
| `.codex-plugin/plugin.json` | **MODIFY** | Bump version to `"0.2.0"` or add `"contract_version": "visual-asset-plugin-contract/1"` field. |

No existing source files (`cli.py`, `render.py`, `art.py`, `vocabulary.py`, `motion.py`, `qa.py`, `benchmark.py`, `scene.py`, `common_briefs.py`) need to be modified. The runner imports and reuses them as-is.

### Q7: Output-dir isolation

**Answer:** The current renderer already guarantees output-dir isolation:

- `_render_asset()` creates `output / output_id / track / route / sequence/` and writes all files there.
- `render_frame()` calls `png_path.parent.mkdir(parents=True, exist_ok=True)`.
- `assemble_mp4()` calls `mp4_path.parent.mkdir(parents=True, exist_ok=True)`.
- The `output` parameter in all render functions is the root; all paths are derived from it.
- `.gitignore` ignores `output/`.

For the Contract V1 runner, the `--output-dir` is Core-owned and passed by the adapter. The runner should:
1. Treat `--output-dir` as the sole output root.
2. Never write outside `--output-dir`.
3. Use the opportunity_id or candidate_id as the subdirectory name.
4. The `--result` file is written by the runner but to a Core-specified path (outside `--output-dir`); it must be written atomically via `temp + os.replace()`.
5. Artifact URIs should use `local-runner://<relative-path>` format (matching Core's `_resolve_artifact()` in `candidate_portfolio.py`).

### Q8: QA/manifest reuse

**Answer:** The following can be directly reused:

| Existing module | Contract V1 reuse |
|---|---|
| `qa.py` → `run_qa(asset_manifest)` | Translates to candidate `qa.status: PASSED` when `run_qa().passed == True`, `FAILED` otherwise. The existing QA checks (provenance, duration 3–10s, files exist, state continuity, V0.2 structural readability) are directly applicable. |
| Per-asset `manifest.json` | Maps to `MANIFEST` artifact role. Already JSON, already contains provenance, track, route, files, sequence SHA-256, and QA report. |
| `contact-sheet.png` | Maps to `PREVIEW` artifact role. |
| `asset.mp4` | Maps to `PRIMARY_MEDIA` artifact role. Needs `media_type: "video/mp4"` and `sha256`. |
| Per-asset manifest's `qa` field | Maps to `QA_REPORT` artifact role (the manifest already contains the QA dict). |
| `sequence_sha256` | Can be used as a deterministic fingerprint; the primary media SHA-256 should be computed separately on the MP4 file bytes. |

What needs adaptation:
- The existing manifest uses `case_id`, `visual_case_id`, `track`, `provenance`, `files`, `sequence_sha256`, `qa`, and optionally `study`, `trial_review`, `spoken_semantics`, `visual_purpose`. The Contract V1 candidate uses `candidate_id`, `asset_family`, `candidate_status`, `duration_ms`, `suggested_placement`, `artifacts`, `qa`, `provenance`, `plugin_metadata`. The runner translates between these shapes.
- The existing `qa.py` does not produce a `qa.status: "PASSED"` or `"FAILED"` string; it produces `{"passed": bool, "failures": [...], "checks": [...]}`. The runner translates: `{"status": "PASSED" if result["passed"] else "FAILED", "summary": "; ".join(result["failures"]) or "all required checks passed"}`.

### Q9: proposal_id / candidate_id deterministic inputs

**Answer:**

**proposal_id** should be derived from plugin-owned deterministic inputs:
```
proposal_id = "prop-im-" + SHA256(
  plugin_id + opportunity_id + suitability + case_mapping + route
)[:24]
```

Where:
- `plugin_id`: `"org.deeptalk.illustrated-metaphor"` (constant)
- `opportunity_id`: from the request
- `suitability`: `"SUITABLE"` / `"BORDERLINE"` / `"ABSTAIN"` (the assessed value)
- `case_mapping`: the `visual_case_id` selected by the suitability function
- `route`: `"approved_still"` or `"structured_hybrid"`

This ensures the same Opportunity always produces the same `proposal_id`, across runs and across Core retries.

**candidate_id** should be derived from:
```
candidate_id = "cand-im-" + SHA256(
  proposal_id + visual_case_id + route + duration_ms + candidate_text
)[:24]
```

Where:
- `proposal_id`: as above
- `visual_case_id`: the mapped case
- `route`: the selected route
- `duration_ms`: the actual rendered duration
- `candidate_text`: the short Chinese label used in the SVG

This ensures that if the same proposal is generated twice, the candidate_id is identical (supporting binary-identical repeatability). A material change in any input (different case mapping, different duration, different text) produces a different candidate_id.

### Q10: Atomic result

**Answer:** The runner must write the result JSON atomically:

```python
import tempfile, os, json

temp_path = result_path.with_suffix(".tmp")
temp_path.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True), encoding="utf-8")
os.replace(temp_path, result_path)
```

This pattern is already used by Core's fake runner (`visual_asset_plugin_fakes.py` lines 64–66). The `os.replace()` call is atomic on POSIX and Windows for same-filesystem replacements.

Additionally, the asset files (MP4, PNG, manifest) should be fully written before the result JSON is written. If any rendering step fails, the runner must:
1. Write a Generation Result with `operation_status: "FAILED"` and a `problem` object.
2. Exit 0 (the Core adapter treats non-zero exit as a process failure, not a plugin FAILED response).
3. Never write a partial result file.

The runner should also handle the suitability case: if suitability assessment fails for any reason, write a Suitability Response with `operation_status: "FAILED"` and a `problem`.

### Q11: Independent plugin version via --version

**Answer:** The runner should establish an independent plugin version:

1. Add `__version__ = "0.2.0-contract-runner"` to `src/illustrated_metaphor/__init__.py`.
2. `scripts/contract_runner.py --version` prints this version string and exits 0.
3. Core's `resolve_plugin_version()` in `visual_plugin_adapter.py` calls `plugin_version_command` and uses the stdout as `plugin_version`. It validates that the output is a single non-empty line.
4. The version string is independent of the `.codex-plugin/plugin.json` version (currently `"0.1.0"`) and independent of any Core release version.
5. Core's adapter validates `response["plugin_version"] == resolved_version`, so the runner must echo this exact version in every response.

Recommended version: `"0.2.0-contract-runner"` — signals that this is the first version with Contract V1 runner support, distinct from the R&D prototype version.

The future implementation session should decide the exact string, but the mechanism is: `__version__` in `__init__.py` → `--version` flag → Core validates match.

### Q12: Fast unit tests

**Answer:** The following can be fast unit tests (no rendering, no FFmpeg, no sips):

| Test | What it covers |
|---|---|
| `test_suitability_returns_suitable_for_accumulation` | Suitability function returns SUITABLE for accumulation/pressure semantics. |
| `test_suitability_returns_borderline_for_causal_chain` | Suitability function returns BORDERLINE for dense causal chain semantics. |
| `test_suitability_returns_abstain_for_numeric_evidence` | Suitability function returns ABSTAIN for exact numeric evidence. |
| `test_case_mapping_selects_burden_for_pressure` | Opportunity→case mapping selects `burden-growth` for pressure/accumulation. |
| `test_case_mapping_selects_tension_for_opposing_forces` | Opportunity→case mapping selects `tug-of-war` for tension. |
| `test_proposal_id_is_deterministic` | Same inputs → same proposal_id. |
| `test_candidate_id_is_deterministic` | Same inputs → same candidate_id. |
| `test_generation_result_has_required_fields` | Generation Result JSON has all Contract V1 required fields. |
| `test_generation_result_candidate_has_primary_media` | Candidate artifacts include PRIMARY_MEDIA with video/mp4. |
| `test_generation_result_placement_within_aroll_window` | suggested_placement is within a_roll_window. |
| `test_qa_translation_passes_when_run_qa_passes` | `run_qa().passed == True` → `qa.status == "PASSED"`. |
| `test_qa_translation_fails_when_run_qa_fails` | `run_qa().passed == False` → `qa.status == "FAILED"`. |
| `test_artifact_uris_use_local_runner_scheme` | All artifact URIs start with `local-runner://`. |
| `test_provenance_origin_is_plugin_generated` | `provenance.origin == "plugin-generated"`. |
| `test_version_flag_outputs_single_line` | `--version` outputs a single non-empty line. |
| `test_suitability_response_correlation` | Response echoes request_id and opportunity_id. |
| `test_abstain_proposal_id_exists_but_no_generation` | ABSTAIN returns proposal_id but generation is never requested. |

All of these test pure functions or JSON shape — no subprocess, no media.

### Q13: Best sanitized dynamic case for real render integration

**Answer:** **CB03 Accumulation Pressure** mapped to a synthetic Opportunity.

Reasons:
1. It is **SUITABLE** — the strongest family fit, no borderline ambiguity.
2. It maps to `burden-growth` — the flagship V0.2 metaphor with a clear actor+object grammar.
3. It uses `structured_hybrid` route — exercises the state-change path, not just a single still.
4. The semantics ("每一轮扩张都会增加新的承诺和资源占用，直到原本分散的压力开始集中出现") are generic and non-private.
5. The Common Brief Trial already has full QA evidence for this case (31/31 pass, repeat hashes match).

The synthetic Opportunity for integration testing:
```json
{
  "opportunity_id": "opp-im-integration-01",
  "spoken_semantics": "持续累积的资源占用使分散的压力开始集中出现。",
  "visual_purpose": "让观众看到积累→压力→临界的变化过程。",
  "a_roll_window": {"start_ms": 12000, "end_ms": 17000},
  "target_duration_ms": 5000,
  "language": "zh-CN",
  "canvas": {"width": 1920, "height": 1080}
}
```

Expected outcome:
- Suitability: `SUITABLE`
- Case mapping: `burden-growth`
- Route: `structured_hybrid`
- Duration: ~5000ms (3 scene states × ~1.67s each)
- Candidate status: `READY`
- QA: `PASSED`
- Artifacts: `PRIMARY_MEDIA` (MP4), `PREVIEW` (contact sheet), `MANIFEST` (JSON), `QA_REPORT` (JSON)
- Placement: within `a_roll_window`

### Q14: Binary-identical fresh runs

**Answer:** Yes, two fresh runs can achieve binary-identical output, with conditions:

**Already deterministic (evidenced):**
- SVG generation is pure string formatting from hardcoded parameters — no randomness.
- `sips` SVG→PNG on macOS is deterministic for the same SVG input.
- FFmpeg with explicit `-framerate`, `-r 24`, `-pix_fmt yuv420p`, `-movflags +faststart`, and no variable bitrate is deterministic.
- The existing project has verified this: "31/31 matching sequence SHA-256 values" and "42 rerendered assets; all sequence SHA-256 values match."
- `sequence_sha256` is computed from `b"".join(Path(item).read_bytes() for item in files[2:])` — ordered, deterministic.

**Conditions for binary-identical Contract V1 results:**
1. Same Opportunity input → same `visual_case_id`, `route`, `candidate_text`.
2. Same case → same SVG → same PNG → same MP4 → same SHA-256.
3. Same `proposal_id` and `candidate_id` (deterministic from inputs).
4. Same `suggested_placement` (derived from `a_roll_window`, not random).
5. Same `duration_ms` (derived from `target_duration_ms` / FFmpeg encoding).
6. Same artifact URIs (deterministic relative paths).
7. `sort_keys=True` in JSON serialization (matching Core's fake runner pattern).

**Risk to binary identity:**
- **FFmpeg metadata timestamps:** FFmpeg may embed creation time in MP4 metadata. The existing renderer does not pass `-metadata creation_time=0`. This should be added in the runner to ensure binary-identical MP4s. Alternatively, the runner can strip metadata with `-map_metadata -1`.
- **sips version:** If macOS or sips is updated between runs, PNG output might change. This is an environmental constant, not a runner concern.
- **Canvas scaling:** If the runner scales 1280×720 SVG to 1920×1080, the scaling algorithm must be deterministic (FFmpeg `-vf scale=1920:1080` is deterministic).

**Recommendation:** Add `-metadata creation_time=1970-01-01T00:00:00.000Z` and `-map_metadata -1` to FFmpeg commands in the runner path, or document that MP4 metadata timestamps may vary while content hashes remain identical.

### Q15: Current most likely blockers

**Answer:**

1. **Canvas mismatch:** Current renderer outputs 1280×720; Contract V1 Opportunities specify 1920×1080. The runner must scale. This is a low-risk blocker — FFmpeg can scale deterministically.

2. **macOS dependency:** `sips` is macOS-only. Core's adapter runs locally on macOS (evidenced by the existing pipeline), but this limits portability. Not a blocker for the current environment, but should be documented.

3. **Duration quantization:** `target_duration_ms` from Core may not be evenly divisible by the number of scene states. The runner should clamp to 3–10 seconds and distribute frames. The existing QA checks `3 <= duration <= 10`.

4. **Suitability assessment ambiguity:** Dynamic Opportunities won't map cleanly to the eight Common Brief patterns. The keyword matcher needs careful design to avoid false SUITABLE on numeric-evidence requests. The ABSTAIN path for numeric evidence is the highest-risk suitability decision.

5. **No `contract_runner.py` exists yet:** The Core example config references `scripts/contract_runner.py` but this file does not exist in the repository. It must be created from scratch.

6. **No `--version` mechanism exists:** `__init__.py` has no `__version__`. The runner must add this.

7. **Atomic result writing pattern:** The existing `cli.py` writes manifests non-atomically (`write_text` directly). The runner must use `temp + os.replace()`.

8. **Canvas in SVG:** The SVG has `width="1280" height="720"` hardcoded. The runner should either modify the SVG generation to accept a canvas parameter (requires modifying `art.py`) or render at 1280×720 and scale via FFmpeg. The latter avoids modifying production source.

### Q16: Where NOT to copy MG internals

**Answer:**

1. **Do not copy MG's Remotion/Node-based rendering pipeline.** MG uses Remotion compositions with Chrome/SwiftShader. Illustrated Metaphor uses Python SVG + sips + FFmpeg. These are fundamentally different renderers.

2. **Do not copy MG's `mg-scene/1` grammar or profile system.** MG has its own scene grammar (`delta-metric`, `editorial-cn-v1`). Illustrated Metaphor has its own `MetaphorSpec` vocabulary (load, barrier, bridge, container, etc.).

3. **Do not copy MG's contract runner architecture if MG has one.** Each plugin owns its own runner. The runner should be built from Illustrated Metaphor's existing modules, not from MG's.

4. **Do not copy MG's QA checks.** MG has media/structural QA specific to Remotion output. Illustrated Metaphor has provenance, duration, state continuity, focal clarity, object count, annotation density, actor/object separation, clutter candidate, and final-frame readability checks.

5. **Do not copy MG's artifact structure.** MG may produce different artifact types (Remotion compositions, frame sequences). Illustrated Metaphor produces SVG, PNG, MP4, contact sheet, and manifest.

6. **Do not import or reference MG's plugin_id, version, or configuration.** Each plugin has independent identity.

7. **Do not copy MG's suitability logic.** MG marked all eight CBs as SUITABLE. Illustrated Metaphor has a different capability boundary with ABSTAIN on numeric evidence.

### Q17: Illustrated Metaphor family identity

**Answer:**

The runner must preserve Illustrated Metaphor's family identity:

1. **asset_family:** `"Illustrated Metaphor"` — the display string in the candidate. Not `"MG"`, `"Hand-drawn"`, or any other family.

2. **plugin_id:** `"org.deeptalk.illustrated-metaphor"` — the Core configuration identifier. Matches the example config.

3. **Visual language:** The B1 V0.2 paper-collage metaphor system: cobalt torso, coral action planes, charcoal grounding, pale-green state objects, warm-white editorial field. This is visually distinct from MG's Remotion compositions and Hand-drawn's SVG illustrations.

4. **Metaphor vocabulary:** load, barrier, bridge, container, stack, rope, wheel, threshold, crack, network node, path, gate, resource block, signal card. These are original SVG primitives, not upstream assets.

5. **Actor grammar:** Anonymous generic actor (no name, face, personality, or fixed identity). Object-only where an actor would mislead (e.g., network propagation).

6. **Suitability boundary:** Strong at physical metaphor, agency/tension, loops, surface-vs-mechanism, and state changes. Weak at exact numeric evidence, dense causal chains, and conditional logical judgments. CB08 Numeric Evidence is a positive ABSTAIN.

7. **Deterministic text:** Chinese labels are SVG/PingFang text, not image-model text. This is a family identity trait: deterministic typography, not generative text.

8. **provenance:** `"original-metaphor-system"` — the existing provenance string. Maps to Contract V1 `provenance.origin: "plugin-generated"` and `provenance.source_ref: "illustrated-metaphor manifest"`.

9. **Route identity:** `approved_still` (final readable state → fade + focal push + hold) and `structured_hybrid` (ordered state cuts). These are Illustrated Metaphor's own route names; they should not be renamed to match MG or Hand-drawn route names.

---

## Proposed runner files

| File | Type | Lines (est.) | Responsibility |
|---|---|---|---|
| `scripts/contract_runner.py` | NEW | ~120 | CLI entry: `--version`, `--request`, `--result`, `--output-dir`. Routes to suitability/generation. Atomic result write. |
| `src/illustrated_metaphor/contract.py` | NEW | ~250 | Pure functions: `assess_suitability(opportunity)`, `map_opportunity_to_case(opportunity)`, `build_suitability_response(request, ...)`, `build_generation_result(request, output_dir)`, `translate_qa(qa_result)`, `build_artifacts(asset, output_dir)`. |
| `src/illustrated_metaphor/__init__.py` | MODIFY | +1 | Add `__version__ = "0.2.0-contract-runner"`. |
| `tests/test_contract.py` | NEW | ~200 | Fast unit tests for all pure functions in `contract.py`. |
| `.codex-plugin/plugin.json` | MODIFY | +1 | Bump version or add contract_version field. |

## Proposed tests

### Fast unit tests (no rendering)

```
test_contract.py:
  - test_suitability_suitable_for_accumulation
  - test_suitability_suitable_for_feedback_loop
  - test_suitability_suitable_for_tension
  - test_suitability_suitable_for_surface_vs_mechanism
  - test_suitability_borderline_for_core_judgment
  - test_suitability_borderline_for_causal_chain
  - test_suitability_borderline_for_rule_change
  - test_suitability_abstain_for_numeric_evidence
  - test_case_mapping_for_each_benchmark_pattern
  - test_proposal_id_deterministic
  - test_candidate_id_deterministic
  - test_suitability_response_shape
  - test_generation_result_shape
  - test_candidate_has_primary_media
  - test_candidate_has_manifest_and_qa_report
  - test_placement_within_aroll_window
  - test_qa_translation_passed
  - test_qa_translation_failed
  - test_artifact_uris_use_local_runner_scheme
  - test_provenance_origin_plugin_generated
  - test_version_single_line
```

### Render integration test (requires sips + ffmpeg)

```
test_contract_runner_integration.py:
  - test_synthetic_accumulation_opportunity_renders_ready_candidate
    (CB03-mapped synthetic Opportunity → SUITABLE → READY candidate with MP4)
  - test_two_fresh_runs_produce_identical_sha256
    (Same Opportunity rendered twice → same primary media SHA-256)
  - test_abstain_opportunity_returns_no_candidate
    (Numeric evidence Opportunity → ABSTAIN → no generation call)
```

## Proposed real synthetic integration case

**CB03 Accumulation Pressure → Synthetic Opportunity:**

```json
{
  "opportunity_id": "opp-im-synthetic-01",
  "spoken_semantics": "持续累积的资源占用使分散的压力开始集中出现。",
  "visual_purpose": "让观众看到积累→压力→临界的变化过程。",
  "a_roll_window": {"start_ms": 12000, "end_ms": 17000},
  "target_duration_ms": 5000,
  "language": "zh-CN",
  "canvas": {"width": 1920, "height": 1080}
}
```

Expected:
- Suitability: `SUITABLE`
- Case: `burden-growth`
- Route: `structured_hybrid`
- Candidate: `READY`, `duration_ms: 5000`, `qa.status: PASSED`
- Artifacts: PRIMARY_MEDIA (MP4), PREVIEW (contact sheet), MANIFEST (JSON), QA_REPORT (JSON)
- Placement: `{"start_ms": 12000, "end_ms": 17000}`

## Deterministic/repeatability assessment

**Already proven deterministic:**
- SVG generation: pure string formatting, no randomness.
- PNG rasterization: `sips` is deterministic for identical SVG input.
- MP4 assembly: FFmpeg with fixed flags produces identical output for identical input frames.
- Sequence SHA-256: 31/31 matching hashes across two fresh runs (V0.2 evidence).
- Common Brief Trial: 7/7 matching hashes.

**Contract V1 runner additions needed:**
1. Add `-map_metadata -1` to FFmpeg to strip variable timestamps from MP4.
2. Use `sort_keys=True` and `separators=(",", ":")` in all JSON serialization.
3. Derive `proposal_id` and `candidate_id` from deterministic inputs only.
4. Derive `suggested_placement` from `a_roll_window` deterministically (use the full window or a deterministic sub-window).
5. Derive `candidate_text` deterministically from `spoken_semantics` (first clause or keyword extraction).

**Verdict:** Two fresh runs of the same Opportunity will produce binary-identical primary media SHA-256 values, given the same macOS/sips/ffmpeg environment. The MP4 file bytes may differ in metadata headers unless `-map_metadata -1` is added.

## Output-dir/path-safety design

1. The runner receives `--output-dir` from Core and treats it as the sole output root.
2. All file writes go to `--output-dir / <candidate_id> / ...`.
3. The runner never writes to paths outside `--output-dir`, except the `--result` file.
4. The `--result` file is written atomically via `temp_path.write_text() + os.replace(temp_path, result_path)`.
5. Artifact URIs use `local-runner://<relative-path>` format, where `<relative-path>` is relative to `--output-dir`.
6. The runner rejects any path traversal in the Opportunity or request (opportunity_id, candidate_id must be safe identifiers).
7. Core's `_resolve_artifact()` already validates `local-runner://` URIs: rejects absolute paths, `..`, symlinks, and verifies containment.

## QA/manifest reuse

| Existing artifact | Contract V1 artifact role | Translation |
|---|---|---|
| `asset.mp4` | PRIMARY_MEDIA | Add `media_type: "video/mp4"`, `sha256`, `duration_ms`. URI: `local-runner://<candidate_id>/b1_metaphor_system/<route>/asset.mp4`. |
| `contact-sheet.png` | PREVIEW | Add `media_type: "image/png"`. URI: `local-runner://<candidate_id>/b1_metaphor_system/<route>/contact-sheet.png`. |
| `manifest.json` | MANIFEST | Add `media_type: "application/json"`. URI: `local-runner://<candidate_id>/b1_metaphor_system/<route>/manifest.json`. |
| `qa` dict in manifest | QA_REPORT | Extract `qa` dict, add `media_type: "application/json"`. URI: same as MANIFEST or separate `qa.json`. |
| `run_qa()` result | candidate `qa` field | `{"status": "PASSED" if result["passed"] else "FAILED", "summary": ...}`. |

## Blockers/risks

| Risk | Severity | Mitigation |
|---|---|---|
| Canvas 1280×720 vs 1920×1080 | Low | FFmpeg scale filter or modify SVG viewBox. Prefer FFmpeg scaling to avoid modifying production source. |
| sips macOS-only | Low (environment) | Document as macOS-only. Not a blocker for current environment. |
| Suitability keyword matcher false positives | Medium | Carefully design ABSTAIN triggers (numeric keywords, percentage patterns). Test against all eight CB patterns. |
| FFmpeg metadata timestamps | Low | Add `-map_metadata -1` to FFmpeg commands in runner path. |
| duration_ms quantization | Low | Clamp to 3–10s, round to nearest frame count. Report actual duration. |
| No existing contract_runner.py | Expected | This is the implementation work. The readiness plan is complete. |
| plugin_version not defined | Low | Add `__version__` to `__init__.py`. |

## Exact recommendation for future implementation

1. **Create `scripts/contract_runner.py`** as the sole entry point. It handles `--version`, `--request`, `--result`, `--output-dir`. It routes to suitability or generation based on `proposal_id` presence in the request.

2. **Create `src/illustrated_metaphor/contract.py`** with pure functions:
   - `assess_suitability(opportunity: dict) -> tuple[str, str, str]` → (suitability, reason, visual_case_id)
   - `map_to_route(visual_case_id: str, suitability: str) -> str` → route name
   - `build_suitability_response(request: dict, ...) -> dict` → Contract V1 suitability response
   - `build_generation_result(request: dict, output_dir: Path) -> dict` → Contract V1 generation result
   - `translate_qa(qa_result: dict) -> dict` → `{"status": "PASSED"/"FAILED", "summary": ...}`
   - `build_artifacts(asset: dict, output_dir: Path, candidate_id: str) -> list[dict]` → artifact list
   - `compute_proposal_id(plugin_id, opportunity_id, suitability, case_id, route) -> str`
   - `compute_candidate_id(proposal_id, case_id, route, duration_ms, text) -> str`

3. **Add `__version__` to `__init__.py`**: `"0.2.0-contract-runner"`.

4. **Do NOT modify** `cli.py`, `render.py`, `art.py`, `vocabulary.py`, `motion.py`, `qa.py`, `benchmark.py`, `scene.py`, `common_briefs.py`. Import and reuse them.

5. **In `contract_runner.py`, for generation:**
   - Parse the Opportunity from the request.
   - Call `assess_suitability()` to get the case mapping (this is consistent with the suitability call).
   - Build a minimal case dict from the mapped `visual_case_id`.
   - Call `_render_asset()` from `cli.py` to produce the actual asset.
   - Translate the asset manifest to Contract V1 format.
   - Write the result atomically.

6. **For `--version`:** Print `__version__` and exit 0.

7. **For suitability:** Never render. Return `COMPLETED` with `suitability`, `reason`, `proposal_id`. For ABSTAIN, `proposal_id` still exists as an audit record.

8. **For generation:** Always produce one actual asset. If rendering fails, return `FAILED` with a `problem`. If QA fails, return `COMPLETED` with `candidate_status: QA_REJECTED`.

9. **Test plan:** 20+ fast unit tests in `test_contract.py`. 3 integration tests in `test_contract_runner_integration.py` (requires sips + ffmpeg).

10. **Determinism:** Add `-map_metadata -1` to FFmpeg in the runner's generation path (not in the existing `render.py` — do it in the runner or as a post-processing step).

## Confirmation

- **No production source changed:** This plan adds only new files (`scripts/contract_runner.py`, `src/illustrated_metaphor/contract.py`, `tests/test_contract.py`) and makes one trivial modification (`__init__.py` +1 line, `.codex-plugin/plugin.json` +1 field). No existing render/art/vocabulary/motion/qa/benchmark/scene/common_briefs module is modified.
- **Core/other plugins untouched:** `HWang0310/deep-talk-studio` was read-only at `d1c990c25e44aa55ffc2789f7b00ee2374a198be`. No other plugin repository was modified.
- **No main/tag/release:** This is a docs-only research branch `agent/contract-v1-runner-readiness`. No merge to main, no tag, no release.
