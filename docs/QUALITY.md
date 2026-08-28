# Quality

V0 QA checks source provenance, 3–10 second duration, declared-output presence, ordered state continuity, deterministic sequence hashes, composition bounds, and route metadata. The full local run produced 42 assets with 42 passing QA reports; a repeat run produced equal sequence hashes for all 42 assets.

Chinese labels are deliberately rendered as SVG text with the local PingFang stack and rasterized by macOS `sips`. This is verified for the deterministic path. The two model-generated stills deliberately contain no text, so image-model Chinese correctness remains unverified and is treated as a generation risk, not a passed gate.

Character/frame consistency is verified only for the deterministic state renderer. It is not verified for independently generated model keyframes. QA also cannot judge subjective metaphor clarity without a human review pass.

## V0.1 additions

The renderer now verifies case-specific metaphor grammar in unit tests and end-to-end SVG output, preventing a benchmark from silently changing only its label. Candidate Track B assets require `original-language-hypothesis` provenance. Final V0.1 output has 35/35 passing manifest QA reports and a final repeat corpus with matching sequence hashes.

The model consistency probe is a visual QA observation, not an automated pass: it passed broad material/palette/semantic recognition but failed strict layout and proportion identity. Model-generated Chinese was not requested and is not passed as a capability.

## V0.2 structural readability QA

V0.2 adds B1-system manifest checks for original-system provenance, a named focal object, 1–4 objects, one sparse semantic annotation, actor/object separation whenever an actor is present, no declared clutter candidate, and a final-frame readability candidate. These checks are deliberately structural: they catch missing composition information, but cannot certify aesthetics or human comprehension.

The current V0.2 corpus has 31/31 passing QA reports. A fresh repeat corpus has matching frame-sequence SHA-256 values for all 31 assets. Two sampled MP4s—state-transition approved-still and information-overload structured-state—both measured 5.000000 seconds. Chinese remained deterministic SVG/PingFang text and was visually inspected as correct in the PNG contact sheets.

Autonomous visual review found the B1 V0.2 final state legible for all seven target claims after correcting the approved-still source to use the final readable scene state; the hidden-fragility crack is now visible rather than latent. The generic actor helps burden, tension, loop, overload, and transition; object-only network avoids inventing agency where the claim is propagation. B2 remains useful for actor-free systems but is not a competing primary direction, so no creator A/B choice was warranted.
