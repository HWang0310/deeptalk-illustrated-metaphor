# Quality

V0 QA checks source provenance, 3–10 second duration, declared-output presence, ordered state continuity, deterministic sequence hashes, composition bounds, and route metadata. The full local run produced 42 assets with 42 passing QA reports; a repeat run produced equal sequence hashes for all 42 assets.

Chinese labels are deliberately rendered as SVG text with the local PingFang stack and rasterized by macOS `sips`. This is verified for the deterministic path. The two model-generated stills deliberately contain no text, so image-model Chinese correctness remains unverified and is treated as a generation risk, not a passed gate.

Character/frame consistency is verified only for the deterministic state renderer. It is not verified for independently generated model keyframes. QA also cannot judge subjective metaphor clarity without a human review pass.

## V0.1 additions

The renderer now verifies case-specific metaphor grammar in unit tests and end-to-end SVG output, preventing a benchmark from silently changing only its label. Candidate Track B assets require `original-language-hypothesis` provenance. Final V0.1 output has 35/35 passing manifest QA reports and a final repeat corpus with matching sequence hashes.

The model consistency probe is a visual QA observation, not an automated pass: it passed broad material/palette/semantic recognition but failed strict layout and proportion identity. Model-generated Chinese was not requested and is not passed as a capability.
