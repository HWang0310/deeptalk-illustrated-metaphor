# DeepTalk Integration Boundary — Illustrated Metaphor

## Purpose

This file defines the compatibility gate that every Illustrated Metaphor optimization must pass before DeepTalk Nexus may repin Core to a new exact SHA.

The plugin may evolve its internal visual language substantially. Better visuals are welcome; silent breakage of the DeepTalk plugin boundary is not.

## Current accepted interface

- Canonical identity: **Illustrated Metaphor**
- Contract version: `visual-asset-plugin-contract/1`
- Runtime behavior baseline: `48848affe018fc2cff8ee15bad7a09bb002776e4`
- Canonical runner: `python3 scripts/contract_runner.py`
- DeepTalk compatibility baseline: `HWang0310/deep-talk-studio@db172cecc60ca6b0c276ec42010b113a767bc7b3`

## Non-negotiable compatibility gate

Unless DeepTalk Nexus separately approves a new versioned contract, Illustrated Metaphor must preserve:

1. independent repository ownership; DeepTalk Core does not import plugin internals;
2. `visual-asset-plugin-contract/1` request/result semantics;
3. two-stage `Suitability -> Generation` behavior;
4. completed suitability outcomes `SUITABLE | BORDERLINE | ABSTAIN`;
5. generation operation statuses `COMPLETED | FAILED | BLOCKED | UNAVAILABLE`;
6. produced candidate statuses `READY | QA_REJECTED`;
7. ordinary subprocess/file invocation through the canonical runner;
8. Core-owned request/result/output-directory boundaries;
9. fail-closed validation for malformed/unsafe requests and outputs;
10. no Codex-only, TeleAgent-only, ChatGPT-only, or other single-Agent proprietary runtime prerequisite;
11. no automatic winner selection, overlap resolution, NLE editing, or A-roll modification;
12. generated metaphor media remains honest illustration and does not impersonate evidence or `REAL_MATERIAL`.

If optimization appears to require breaking this boundary, stop and escalate rather than silently changing it.

## Plugin-local optimization freedom

Within the gate, the project may independently evolve:

- metaphor/object/action vocabulary;
- semantic relation → composition mapping;
- scene variation and visual anchors;
- actor/object grammar;
- deterministic render internals;
- typography and annotation placement;
- motion timing and transitions;
- suitability/abstention heuristics, provided Contract semantics remain compatible;
- benchmark corpus and creator-facing visual QA.

Track A provenance restrictions remain separate from DeepTalk compatibility and must continue to be respected.

## Required validation before handback

Before a Plugin Curator reports a candidate runtime ready for DeepTalk review:

- project-native tests and lint/quality checks pass;
- representative render/QA paths pass;
- canonical runner `--version`, suitability, and generation smoke paths pass;
- resulting Contract V1 response and artifacts validate against the approved Core compatibility baseline;
- no private episode material or machine-specific secrets are committed;
- provenance boundaries remain correct;
- representative before/after visual evidence is available for Owner review;
- branch and remote exact SHA are available for independent review;
- any change to identity/version/runner/artifact roles/status semantics is explicitly declared.

## Handback protocol

```text
PLUGIN_OPTIMIZATION_READY
PLUGIN: Illustrated Metaphor
REPO: HWang0310/deeptalk-illustrated-metaphor
BASE_SHA: <starting main SHA>
CANDIDATE_SHA: <full exact SHA>
BRANCH: <task branch>
RUNNER: python3 scripts/contract_runner.py
CONTRACT_V1_COMPAT: PASS/FAIL
DEEPTALK_CORE_BASE: db172cecc60ca6b0c276ec42010b113a767bc7b3
CORE_INTEGRATION_CHECK: PASS/FAIL
NATIVE_VALIDATION: PASS/FAIL
OWNER_VISUAL_REVIEW: PASS/PENDING
BREAKING_CHANGE: NONE/<brief>
BLOCKER: NONE/<brief>
```

The Plugin Curator may decide that the Illustrated Metaphor project itself has reached an accepted quality milestone. Only DeepTalk Nexus may update the Core pin after an independent exact-SHA integration review.
