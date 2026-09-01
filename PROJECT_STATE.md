---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: '84d8a35b-d64d-4386-beaa-6ba3820d4e63'
  PropagateID: '84d8a35b-d64d-4386-beaa-6ba3820d4e63'
  ReservedCode1: '5fb59a97-39fd-439e-b1a6-54b1101b60dc'
  ReservedCode2: '5fb59a97-39fd-439e-b1a6-54b1101b60dc'
---

# Project State

**Updated:** 2026-09-01 — Visual Asset Plugin Contract V1 runner implemented (CORRECTION-1 applied), awaiting Nexus review.

## Current truth

- Repository initialized on `main`; public GitHub remote is configured.
- V0 is a standalone dual-track R&D project. DeepTalk Core is out of scope and must remain unmodified.
- The approved baseline is deterministic motion assembly from an approved still. Structured scene states and independent keyframes are comparison routes.
- Upstream audit is complete at `91b560849e8f883922cc2fa8a358a668caa94105`; Track A provenance and attribution boundary are documented.
- Seven benchmark cases produced 42 deterministic MP4 assets across two tracks and three routes. A repeated corpus has equal sequence SHA-256 values.
- Two no-user-key model stills were generated as separate candidates. Model image-text and independent-keyframe consistency remain unverified.
- A minimal plugin manifest validates the repository shape without defining a DeepTalk Core contract.
- Initial V0 evidence commit: `2455b24818969e128798d3451db2b27a12c2d226`; check Git for current HEAD.
- ChatGPT Product Review marked V0 R&D PASS and froze Track A as reference. Track B is now primary R&D.
- V0.1 compared B1 Paper Relay and B2 Object Theatre on the same seven benchmarks. B1 is the current research baseline, with a generic actor grammar rather than a mascot.
- Final V0.1 corpus has 35 assets and matching sequence hashes on repeat. The small B1 model study shows recognizable but insufficiently exact two-state consistency.
- V0.1 implementation commit: `91e3afab8b3fa250fafc32c64893e8e8f5ad4085`; check Git for current HEAD.
- V0.2 promotes B1 from a rendering hypothesis to a bounded original metaphor system: seven immutable specs define actor/object roles, spatial relation, focal point, state change, annotation placement, and motion opportunity. The generic actor stays anonymous; network effect is deliberately object-only.
- V0.2 uses a first composable original vocabulary—load, barrier, bridge, container, stack, rope, wheel, threshold, crack, network node, path, gate, resource block, and signal card—implemented as project-owned SVG primitives, not upstream assets.
- The V0.2 comparison corpus has 31 assets: 28 approved-still comparator assets across Track A, B1 V0.1, B1 V0.2, and B2; plus three selective B1 V0.2 structured-state assets. Fresh QA is 31/31 pass and repeat sequence hashes are 31/31 equal.
- B1 V0.2 is the current Track B research baseline. It is not a formal brand identity, mascot, or original character IP declaration. Track A remains frozen upstream reference; B2 remains a useful secondary actor-free comparator.
- Common Brief Trial is complete as a comparison experiment, not V0.3: CB01/CB02/CB07 are BORDERLINE, CB03–CB06 are SUITABLE, and CB08 Numeric Evidence is an explicit ABSTAIN. Seven B1 assets are generated under `output/common-brief-trial/`; B2 and Track A generate no Common Brief asset.
- The trial confirms family strengths in physical metaphor, agency, tension, feedback, and state change. It confirms limits in exact numbers, dense causal chains, and conditional logical judgments. No MG or Hand-drawn trial repository or output was inspected.

## Visual Asset Plugin Contract V1 Runner

- TASK_ID: DT-ILL-CV1-001
- Implementation branch: `agent/contract-v1-runner-implementation`
- Starting readiness SHA: `6f2af7d8da454ac061a8040242c6b4b66fc34d48`
- Status: IMPLEMENTED_UNRELEASED / AWAITING_NEXUS_REVIEW
- The Contract V1 runner implements the full Visual Asset Plugin Contract V1 specification:
  - Deterministic suitability assessment (SUITABLE/BORDERLINE/ABSTAIN) via keyword matching
  - Deterministic proposal_id and candidate_id computation (SHA-256 based)
  - Real asset rendering via the existing SVG → sips → ffmpeg pipeline
  - Actual MP4 duration measurement via ffprobe; Candidate.duration_ms reflects real media
  - QA re-run on final post-processed artifacts (not pre-postprocess QA)
  - ABSTAIN generation fails closed (FAILED with SUITABILITY_ABSTAIN, no Candidate)
  - Canvas quality-first: 1920x1080 via SVG vector re-rasterization; non-16:9 → BLOCKED
  - MP4 metadata stripped (`-map_metadata -1`) for binary repeatability
  - Atomic result write (temp + os.replace)
  - 73+ tests pass (25 existing + 38 unit + 10+ integration), ruff clean
- Nexus reviewed initial implementation at SHA `06e938ed`; CORRECTION-1 applied for 5 issues:
  1. Candidate duration reflects actual MP4 (ffprobe measurement)
  2. Real 1920x1080 CLI integration test (frame/MP4 actual resolution verified)
  3. QA runs on final post-processed artifacts
  4. ABSTAIN generation fails closed
  5. PROJECT_STATE.md updated
- Not ACCEPTED, not PINNED, not RELEASED. Awaiting Nexus exact-SHA review.

## Next operational action

Do not enter a next stage from this trial. Any future Product Review may use the evidence to decide whether a separate creator-usability study is warranted; do not promote B1 to a formal brand identity, mascot, or production model-keyframe pipeline.