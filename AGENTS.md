# Illustrated Metaphor Agent Guide

## Scope

`deeptalk-illustrated-metaphor` is a standalone R&D repository for turning cognitive metaphors into short illustrated motion assets. Its canonical identity is **Illustrated Metaphor**. It must not modify, import, or couple to DeepTalk Core during V0.

## Fresh Agent Bootstrap

1. Read `PROJECT_STATE.md` first; it is the current operational truth.
2. Read `README.md`, `docs/INDEX.md`, and the latest entry in `HANDOFF.md`.
3. Check `git status --short`, `git log --oneline -5`, and the latest render evidence in `output/` if present.
4. Treat `docs/plans/*-xiaohei-upstream-audit.md` and `THIRD_PARTY_NOTICES.md` as the provenance boundary for Track A.
5. Keep generated media under `output/` and never commit it unless an explicit request changes this policy.
6. Preserve the separation: Track A is an upstream-reference experiment; Track B is an independent neutral/original experiment. Never present Xiaohei / 小黑 as DeepTalk IP.

## Engineering Rules

- Run unit tests before every commit; run a full render before claims about visual output.
- Use deterministic, no-key paths as the V0 baseline. Clearly label optional image-generation gaps.
- Preserve benchmark inputs and render manifests so results can be reproduced.
- Do not design a final cross-plugin contract or edit `../deep-talk-studio`.
