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

> Current operational truth. GitHub remote and exact reviewed SHAs override chat or local workspace claims.

## Identity

| Field | Current truth |
| --- | --- |
| Repository | `HWang0310/deeptalk-illustrated-metaphor` |
| Stable branch | `main` |
| Runtime behavior baseline | `48848affe018fc2cff8ee15bad7a09bb002776e4` |
| Stage | Contract V1 runner `ACCEPTED / IMPLEMENTED_UNRELEASED`; semantic-specificity/visual-quality optimization is the next product track |
| Canonical identity | **Illustrated Metaphor** |
| Canonical runner | `python3 scripts/contract_runner.py` |
| Product boundary | Independent illustrated-metaphor plugin; DeepTalk Core is a separate consumer and may repin only after Nexus integration review |

## Governance

- `main` represents the latest plugin-local accepted stable runtime plus governance-only updates.
- New engineering work starts from `main` on an isolated task branch and follows the current `HWang0310/engineering-journal` standards.
- `AGENTS.md` defines mandatory bootstrap, provenance, and project-specific rules.
- `docs/DEEPTALK-INTEGRATION.md` is the non-negotiable DeepTalk compatibility gate.
- Plugin-local acceptance never updates DeepTalk Core automatically. The plugin returns an exact SHA to DeepTalk Nexus for independent integration review.

## Research / provenance boundary

- Track A remains an upstream-reference research track with explicit provenance and no project ownership claim over Xiaohei / 小黑.
- Track B is the independent neutral/original implementation path and remains the primary project-owned R&D direction.
- The project-owned visual vocabulary and generated media must stay provenance-clean and must not impersonate evidence/REAL_MATERIAL.

## What has been evidenced

- Deterministic local illustrated rendering from approved stills and structured scene states.
- Repeatable benchmark corpora with machine QA and sequence-hash evidence.
- A bounded project-owned original metaphor vocabulary and neutral actor/object grammar.
- Contract V1 suitability/generation behavior at the runtime baseline, including fail-closed ABSTAIN generation handling and real 1920×1080 output validation.
- DeepTalk Phase 5 synthetic integration with the exact-pinned runner.
- Limited real-A-roll Phase 6 owner-visible evidence produced creator-viewable candidates and exposed the current quality weakness: different opportunities can collapse into generic metaphor patterns, while mechanism-heavy content may be represented too abstractly to add enough explanatory value.

## Current quality direction

The next optimization track should prioritize:

- stronger semantic specificity;
- opportunity-specific metaphor/action/composition mapping;
- broader project-owned object/action vocabulary;
- less reuse of generic drag/pull/burden motifs;
- stronger visual anchors for the exact spoken concept;
- better scene variation and motion differentiation;
- explicit `ABSTAIN` when metaphor would reduce factual precision;
- creator-facing before/after benchmarks that evaluate semantic fit as well as aesthetics.

## Known limitations

- Exact numbers and dense causal logic are not natural fits for decorative metaphor and should often abstain.
- Some mechanism opportunities can produce visually coherent but semantically weak metaphors.
- Model-generated independent-keyframe consistency remains a separate high-risk research path, not a production requirement.
- Track A must remain provenance-bounded and must never be treated as project-owned identity.

## Current next gate

Start an independent Illustrated Metaphor optimization Curator session from repository Recovery Issue #1. The plugin project may improve internal rendering and visual language, but completion requires native validation, representative before/after visual evidence, Contract V1 compatibility, provenance correctness, and a handback exact SHA for DeepTalk Nexus integration review.
