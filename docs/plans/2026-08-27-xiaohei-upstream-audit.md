# Xiaohei Upstream Audit — 2026-08-27

## Audit record

- Clone source: `https://github.com/helloianneo/ian-xiaohei-illustrations`
- Actual audited commit: `91b560849e8f883922cc2fa8a358a668caa94105`
- Commit date/message: 2026-06-03, `Commit`
- Local audit clone: `vendor/upstream-audit/ian-xiaohei-illustrations/` (gitignored)

## Files actually inspected

- `README.md`
- `LICENSE`
- `NOTICE.md`
- `ian-xiaohei-illustrations/SKILL.md`
- `ian-xiaohei-illustrations/references/style-dna.md`
- `ian-xiaohei-illustrations/references/xiaohei-ip.md`
- `ian-xiaohei-illustrations/references/composition-patterns.md`
- `ian-xiaohei-illustrations/references/prompt-template.md`
- `ian-xiaohei-illustrations/references/qa-checklist.md`
- `examples/prompts.md`
- example-image inventory under `examples/images/`

## Observed upstream facts

1. The upstream identifies itself as a Codex Skill for Chinese 16:9 article illustrations, not as a generic motion-asset system.
2. Its default visual IP is 小黑: a solid black, white-dot-eyed, deadpan worker that must carry the core conceptual action.
3. Its method emphasizes one cognitive anchor per image, generous white space, sparse short Chinese annotations, constrained red/orange/blue accents, and newly invented physical metaphors.
4. It gives reusable composition classes and an explicit anti-copy rule for its example compositions.
5. It expects image-model generation per image and flags Chinese typo, style drift, excess text, clutter, and decorative-character failure as QA risks.
6. Its code/docs are MIT-licensed. Its notice separately identifies 小黑 as Ian's recurring visual language and asks for name retention or attribution when the repository is redistributed or adapted.

## Our proposal and boundary

Track A studies the method-level combination of single cognitive action, sparse annotation, 16:9 composition, and actor participation. It is always marked `upstream-reference-only`; it does not name, package, or claim 小黑 as this project's identity. Track B tests the same conceptual requirements in an independent neutral collage language. No upstream code, examples, prompts, documentation, or image assets were copied into this repository.

## Implication for V0

The upstream supports a strong still-illustration hypothesis, but provides no evidence for stable multi-frame animation. Motion reliability must therefore be established independently, and must distinguish deterministic assembly from independently generated frames.
