# Quality

V0 QA checks source provenance, 3–10 second duration, declared-output presence, ordered state continuity, deterministic sequence hashes, composition bounds, and route metadata. The full local run produced 42 assets with 42 passing QA reports; a repeat run produced equal sequence hashes for all 42 assets.

Chinese labels are deliberately rendered as SVG text with the local PingFang stack and rasterized by macOS `sips`. This is verified for the deterministic path. The two model-generated stills deliberately contain no text, so image-model Chinese correctness remains unverified and is treated as a generation risk, not a passed gate.

Character/frame consistency is verified only for the deterministic state renderer. It is not verified for independently generated model keyframes. QA also cannot judge subjective metaphor clarity without a human review pass.
