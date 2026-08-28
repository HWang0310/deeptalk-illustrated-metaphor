# Research Findings

## Track A — Xiaohei-inspired reference study

The upstream audit supports the value of a black deadpan actor as a compact carrier of a single cognitive action. A generated still and deterministic reference prototype both make the growing-burden idea readable. However, this track is reference-only: the output must retain provenance and must not become the project's visual identity.

## Track B — neutral/original study

A cobalt/coral/pale-green paper-collage figure also makes the same burden metaphor readable, while being visibly distinct from Track A. This is evidence that the method is not dependent on the specific upstream character. It is not evidence that Track B has a finished original character system; V0 intentionally tests a language, not a frozen IP.

## Motion route comparison

| Route | V0 result | Recommendation |
| --- | --- | --- |
| Approved still + deterministic motion | Stable 4–5 second MP4s; source still, pan/reveal/emphasis plan, labels, duration, and file output are deterministic. | Baseline delivery route. |
| Structured scene-state hybrid | Stable in this deterministic renderer across 2–3 declared states; creates a useful stop-motion comparator. Model-generated state continuity remains unverified. | Explore only after an approved still/scene design. |
| Independent keyframes | The local comparator can assemble independent deterministic states, but no evidence establishes character or style consistency across independently model-generated frames. | High-risk control; do not prioritize engineering. |

## Rendered evidence

- Deterministic corpus: `output/v0/` — 42 MP4 assets, PNG sequences, SVG states, contact sheets, manifests, and QA reports.
- Repeatability corpus: `output/v0-repeat/` — 42 rerendered assets; all sequence SHA-256 values match the first run.
- Model still candidates: `output/v0/generative-stills/track-a-reference-generated-still.png` and `output/v0/generative-stills/track-b-neutral-generated-still.png`.

## No-key feasibility and cost

The local baseline uses Python standard library, macOS `sips`, and FFmpeg; it needs no user API key and rendered all 42 assets in 11.552 seconds on this machine. Built-in image generation also worked without a user-supplied API key for two still candidates, but its latency and monetary accounting are service-managed and therefore not claimed as reproducible local cost. Image generation is optional evidence, not the V0 runtime dependency.

## Current answer

Evidence favors the transferable **Illustrated / Character Metaphor method** over dependence on a particular character identity. Deterministic motion adds enough practical value for 3–10 second talk-video inserts when it is limited to reveal/pan/cut/emphasis. True stop-motion is not yet shown to provide a large enough gain to outweigh model-frame consistency risk.

## V0.1 — original visual-language study

Track A is frozen as the provenance-labelled reference comparator. Track B is primary research. The V0.1 corpus used the unchanged seven-case benchmark and added two original, coherent systems:

| Candidate | Character strategy | Visual grammar | Result |
| --- | --- | --- | --- |
| B1 Paper Relay | Anonymous generic actor; no name, face, personality, or fixed identity | Cobalt torso, coral action planes, charcoal grounding, pale-green state objects, warm-white editorial field | Strongest current research baseline. The actor makes force, responsibility, and state change readable without requiring a mascot. |
| B2 Object Theatre | No recurring actor | Charcoal stage, indigo/coral/yellow geometric objects, high negative space | Useful secondary grammar for systems and relationships; less immediate for effort and agency. |

Each of the seven benchmark cases now uses an explicitly different physical grammar: burden, tension, loop, fragility, overload, network, or transition. The first V0.1 renderer output was rejected as evidence because it reused one layout across all cases; the final corpus corrected this and has seven unique non-text layouts.

### Fixed-character finding

The generic B1 actor improves immediate agency and causal clarity relative to actor-free B2. That does **not** justify a fixed original character: a named or personality-bearing character would add subject-matter constraints, a larger identity burden, and multi-frame consistency cost. Current recommendation: retain a reusable *generic actor grammar*, not a mascot.

### Deterministic motion finding

Approved-still motion is now a real single-still FFmpeg assembly: 0.35-second fade-in, bounded 3.5% focal push, then hold. It is appropriate for unobtrusive talking-head B-roll. Object-specific emphasis is not claimed in this route; use a structured scene state when the state itself must change.

### True stop-motion value

B1 structured-state study covers all seven cases with 2–3 state frames. It visibly improves explanation for accumulation, loops, and thresholds, but its storytelling gain is modest for a 3–5 second insert. Recommendation: retain it as a selective enhancement for state-change concepts, not a default replacement for approved-still motion.

### Small model consistency probe

Two independently generated B1 burden states used a locked anonymous actor/object prompt and no image text. Material, palette, actor components, side placement, and burden semantics remained recognizable. Actor scale, exact limb geometry, margin, and object-to-actor proportion drifted. Result: suitable as research evidence only; not a production multi-state generation baseline.

### V0.1 evidence

- Final deterministic comparison: `output/v0.1/comparison/` — 35 assets: Track A approved-still reference (7), Track B V0 control (7), B1 approved-still plus structured-state (14), and B2 approved-still (7).
- Deterministic repeat: `output/v0.1/repeat-final/` — all 35 sequence hashes match the final comparison corpus.
- Model probe: `output/v0.1/model-consistency/b_paper_relay/start.png` and `overwhelm.png`.
- The final 35-asset repeat rendered in 9.319 seconds on this machine. This is local, no-key deterministic cost only.

## V0.2 — Original Metaphor System

V0.2 moves B1 beyond a shared paper style by treating each benchmark as a reusable cognitive scene grammar. The new `MetaphorSpec` record states the actor role (or object-only choice), original objects, spatial relation, focal object, declared state change, upper-left deterministic annotation, and a possible deterministic motion emphasis. The grammar is intentionally limited to seven benchmark patterns rather than claiming universal coverage.

| Comparator | Evidence from the unchanged benchmark | Current finding |
| --- | --- | --- |
| Track A Xiaohei-inspired reference | Compact black actor and one-action framing remain legible, but upstream identity and provenance constraints remain material. | Frozen reference only; no new implementation investment. |
| B1 Paper Relay V0.1 | Generic actor establishes immediate effort/agency, but its renderer begins from a small set of direct case overlays. | Useful historical baseline, not the preferred reusable system. |
| B1 Original Metaphor System V0.2 | Seven case-specific actor/object/space/focal specifications; 10 B1 assets in the 31-asset corpus; deterministic Chinese and repeatable state logic. | Current Track B research baseline. |
| B2 Object Theatre | Actor-free arrangement preserves negative space and works especially for systems/relationships. | Valuable secondary comparator; weaker for effort, resistance, and responsibility. |

### Generic-actor finding

The reusable anonymous actor improves causal clarity where a person bears, pulls, receives, runs, observes, or chooses. It is intentionally omitted for network propagation. This supports a *generic actor grammar*, not a fixed original character: there is still no face, name, personality, ownership claim, or mascot decision. A fixed character has not shown enough added recognition benefit to offset subject-matter restriction and multi-state consistency cost.

### Deterministic and structured motion

The production baseline remains final approved still → local deterministic assembly: 0.35-second fade-in, bounded 3.5% whole-frame focal push, and hold. V0.2 records a focal target but does not overstate it as component animation. The final readable state is used as the approved still so a single frame carries the central claim.

Structured states make the scale escalation of burden, information accumulation, and threshold crossing easier to follow. They still add only a modest storytelling benefit in a 4–5 second talking-head insert, so the route remains selective rather than default. Independent keyframes remain a high-risk control without new investment.

### Model consistency decision

No new model-generated multi-state probe was run. The V0.1 two-state locked B1 probe already found recognisable material/palette/semantic continuity but layout, limb geometry, margins, and object proportions drifted. V0.2's evidence gain comes from deterministic grammar, not by extending an unproven model production path. Model-generated Chinese remains unverified and intentionally out of scope.

### V0.2 rendered evidence and repeatability

- `output/v0.2/comparison/`: 31 MP4 assets with PNG/SVG source sequences, contact sheets, manifests, and QA reports.
- `output/v0.2/repeat/`: same 31 assets; all frame-sequence SHA-256 values match the comparison corpus.
- Fresh local no-key render time: 8.708 seconds for comparison; 8.459 seconds for repeat on this machine. This measures the SVG → sips → FFmpeg pipeline only; it excludes service-managed image-model latency/cost.

### Current recommendation

Keep B1 Original Metaphor System as the current **Track B research baseline**, without promoting it to a formal DeepTalk identity. Continue approved-still deterministic motion as the primary usable form. Use B1 structured states only for inherently temporal semantic changes. Keep Track A and B2 in comparison evidence. The next Product Review should decide whether to test a modest expanded case set or evaluate creator-facing usability; it should not yet approve a mascot, a final brand language, or a model-keyframe production pipeline.

## Cross-Plugin Common Brief Trial — Illustrated Metaphor track

This is a fixed-eight-brief comparison experiment, not V0.3. The Illustrated Metaphor track did not inspect MG or Hand-drawn trial repositories or output, did not generate a Track A asset, and did not expand the visual language or model pipeline.

The outcome is four SUITABLE candidates (accumulation pressure, feedback loop, two-side tension, surface vs mechanism), three BORDERLINE candidates (core judgment, causal transmission, rule change), and one deliberate ABSTAIN (numeric evidence). Seven B1 assets were rendered; B2 was not used because it was not distinctly more natural for any specific brief. The full per-brief rubric and visual review are in [`docs/COMMON_BRIEF_TRIAL.md`](COMMON_BRIEF_TRIAL.md).

The key capability boundary is now evidenced rather than assumed: this family is strong at physical metaphor, agency, emotional/causal tension, state change, and abstract relationship. It becomes less reliable when exact numbers, dense labelled chains, or narrow conditional logic must remain visually primary. In those cases, an abstention or deterministic data/editorial treatment is preferable to metaphor overreach.
