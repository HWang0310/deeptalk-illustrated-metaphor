# Illustrated Metaphor Agent Guide

## Mandatory bootstrap

At the beginning of every Curator or engineering task:

1. Read the current `HWang0310/engineering-journal` default branch as the cross-project engineering standard source. At minimum follow its `NEW-SESSION-BOOTSTRAP.md` reading order and inherit the Curator/Axiom/Mason/Rivet model, Task ID lifecycle, GitHub-native handoff, exact-SHA review, one-writer/worktree isolation, and restricted-content hard gate.
2. Record the engineering-journal remote exact SHA used for important new phases.
3. Inspect this repository remote/current branch, `git status --short`, `git log --oneline -5`, and current HEAD.
4. Read `PROJECT_STATE.md` first; it is the current operational truth.
5. Read `README.md`, `docs/INDEX.md`, and `docs/DEEPTALK-INTEGRATION.md`.
6. Consult `HANDOFF.md` for history/evidence, not as a substitute for current state.
7. Treat `docs/plans/*-xiaohei-upstream-audit.md` and `THIRD_PARTY_NOTICES.md` as the provenance boundary for Track A.

## Roles and task lifecycle

- Curator owns project management, architecture coordination, task decomposition, technical decisions, Agent routing, exact-SHA Review, acceptance, and merge decisions.
- Mason/Rivet are the default implementation engineers for clear, verifiable work. Axiom is reserved for deep architecture, difficult debugging, high-risk runtime/Contract work, or high-risk review.
- Formal engineering work uses a unique Task ID and follows the lifecycle defined by `engineering-journal`.
- GitHub remote exact SHA is engineering truth. Agent self-report does not equal acceptance.
- Default to one Writer. Parallel Writers require isolated branches/worktrees, no shared mutable state, and no overlapping critical files.

## GitHub-native internal handoff

- This Illustrated Metaphor repository is the canonical durable engineering handoff channel between the browser ChatGPT plugin Curator and engineering Agents.
- Every formal Task ID must be recoverable from repository-native facts: task/issue context when used, branch/worktree, pushed commit(s), remote exact SHA, relevant diff, validation evidence, and Curator Review outcome.
- Normal Agent completion flow is: implement -> validate -> commit -> push -> expose branch + exact SHA. Agent self-report never replaces remote verification.
- When the plugin Curator can access GitHub, the Owner should normally need to report only `Agent + Task ID completed` (or equivalent short completion signal). The Curator must then inspect this repository's remote branch, exact SHA, diff, tests/render/QA evidence, and project state directly.
- Do not require the Owner to relay long technical handoffs when the same durable facts are available in GitHub. If critical evidence exists only locally, request only the minimal supplemental evidence needed and record the resulting durable decision/state back in GitHub.
- ChatGPT, Codex, TeleAgent, or other Agent chat transcripts are not canonical project memory and should not be copied wholesale into the repository. Preserve durable engineering facts and decisions, not full conversations.
- `PROJECT_STATE.md` stores current operational truth; `HANDOFF.md` stores important chronological history/evidence; issues/PRs/commits carry task-specific traceability as appropriate.
- Plugin-internal handoff is separate from cross-project handback. After plugin-local acceptance, use the defined `PLUGIN_OPTIMIZATION_READY` protocol; only DeepTalk Nexus may independently review integration and repin Core.

## Scope and provenance

- `deeptalk-illustrated-metaphor` owns the standalone Illustrated Metaphor visual plugin. It must not modify or import DeepTalk Core internals.
- Track A remains an upstream-reference experiment with explicit provenance. Track B is the independent neutral/original implementation path.
- Never present Xiaohei / 小黑 as DeepTalk IP or as project-owned identity.
- Keep generated media under local ignored output/artifact directories unless a reviewed task explicitly authorizes a small non-private evidence artifact.
- No credentials, private episode material, machine-specific secrets, or proxy settings belong in Git.
- The restricted-content hard gate from `engineering-journal` applies to all source, docs, tests, fixtures, prompts, issues, commits, and generated project-controlled material.

## Engineering rules

- Run unit tests before commit; run representative/full render evidence before claims about visual quality.
- Use deterministic, no-key paths as the baseline unless a reviewed task explicitly introduces another path.
- Preserve benchmark inputs, manifests, and reproducible QA so before/after quality claims can be checked.
- Prefer semantic specificity over generic decorative metaphor; when a useful metaphor would reduce factual precision, `ABSTAIN` is better than filler.
- Plugin optimization is successful only if the resulting exact SHA remains insertable into DeepTalk through `docs/DEEPTALK-INTEGRATION.md`.
- Do not edit `HWang0310/deep-talk-studio` or silently redesign the shared plugin Contract from this repository.
- Before handback, run project-native tests/lint/render/QA, `git diff --check`, restricted-content review, and return branch + remote exact SHA.
