# Cross-Plugin Common Brief Trial — Illustrated Metaphor Track Design

## Scope and isolation

This is a comparison experiment, not V0.3, a plugin contract, a brand exercise, or episode production. It lives entirely in this repository. No MG or Hand-drawn trial repository, file, output, or result is read. Track A remains frozen and receives no Common Brief asset.

The experiment applies the exact eight provided semantic briefs to the current Illustrated Metaphor family. It may say `SUITABLE`, `BORDERLINE`, or `ABSTAIN`; an abstention is a successful finding rather than a missing deliverable.

## Chosen assessment

| Brief | Assessment | Existing family grammar | Candidate decision |
| --- | --- | --- | --- |
| CB01 Core Judgment | BORDERLINE | B1 loop | Render one experimental still; it conveys recursive dependence but not the precise business condition. |
| CB02 Causal Transmission | BORDERLINE | B1 object-only network | Render structured states; node activation can show transmission but sparse illustration cannot fully label a four-step chain. |
| CB03 Accumulation Pressure | SUITABLE | B1 burden/load | Render structured states; expansion and concentration are native physical metaphors. |
| CB04 Feedback Loop | SUITABLE | B1 loop/wheel | Render structured states; the cyclic mechanism is a native family strength, while copy carries the named entities. |
| CB05 Two-side Tension | SUITABLE | B1 rope/two actors | Render approved still; opposing agency and shared constraint are immediately legible. |
| CB06 Surface vs Mechanism | SUITABLE | B1 bridge/crack | Render approved still at final readable state; surface/hidden failure maps directly to the existing grammar. |
| CB07 Rule Change | SUITABLE | B1 gate/threshold/barrier | Render structured states; before/change/after is a native state-transition grammar. |
| CB08 Numeric Evidence | ABSTAIN | none | Do not render. Exact 42% → 58% plus a causal mechanism needs deterministic data/editorial treatment, not a compressed paper metaphor. |

## Runner design

`benchmarks/common-briefs.json` stores the eight briefs verbatim plus the trial decisions and rubric inputs. A small loader validates them. The runner selects the existing V0.2 visual case only for actual candidates, preserves the Common Brief ID as the output directory and manifest ID, and records the existing visual case separately.

The runner writes `output/common-brief-trial/<CB-id>/...` for seven actual candidates: MP4, deterministic PNG/SVG source evidence, contact sheet, individual manifest, and QA. It writes a root manifest containing all eight assessments, including CB08's deliberate abstention. The output directory remains gitignored.

## Evaluation rubric

Each brief record contains suitability; semantic clarity; metaphor clarity; time to understand; family naturalness; emotional/agency usefulness; motion usefulness; Chinese readability; clutter; creator usefulness; generic-actor necessity; object-only decision; selected route; metaphor-overreach finding; and rationale. These are autonomous research judgements, not model-generated scores or a new external comparison contract.

## Constraints

- Use B1 Original Metaphor System for every actual candidate.
- B2 is not used unless distinctly more natural; this brief set does not justify it.
- Do not create a mascot, fixed character, visual brand, new image-model pipeline, or Track A asset.
- Preserve approved-still deterministic motion as baseline; use structured state only for CB02, CB03, CB04, and CB07.
- Keep Chinese deterministic SVG text.
- Do not inspect another plugin's trial outputs.
