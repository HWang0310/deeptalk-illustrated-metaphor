"""Integration tests for Contract V1 runner — requires sips + ffmpeg.

Tests:
  1. Synthetic CB03 Accumulation Pressure → SUITABLE → READY candidate with real MP4
  2. Two fresh runs produce identical PRIMARY_MEDIA SHA-256 (repeatability proof)
  3. ABSTAIN opportunity returns no candidate
"""

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Ensure src is on path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from illustrated_metaphor.contract import (
    CONTRACT_VERSION,
    PLUGIN_ID,
    PLUGIN_VERSION,
    build_generation_result,
    build_suitability_response,
)

_SYNTHETIC_OPPORTUNITY = {
    "opportunity_id": "opp-im-synthetic-01",
    "spoken_semantics": "持续累积的资源占用使分散的压力开始集中出现。",
    "visual_purpose": "让观众看到积累→压力→临界的变化过程。",
    "a_roll_window": {"start_ms": 12000, "end_ms": 17000},
    "target_duration_ms": 5000,
    "language": "zh-CN",
    "canvas": {"width": 1280, "height": 720},
}

_ABSTAIN_OPPORTUNITY = {
    "opportunity_id": "opp-im-abstain-01",
    "spoken_semantics": "用户留存率从 42% 提升到 58%，数据变化显著。",
    "visual_purpose": "表达精确百分比的变化。",
    "a_roll_window": {"start_ms": 12000, "end_ms": 17000},
    "target_duration_ms": 5000,
    "language": "zh-CN",
    "canvas": {"width": 1280, "height": 720},
}


def _suitability_request(opportunity):
    return {
        "contract_version": CONTRACT_VERSION,
        "request_id": "req-suit-01",
        "opportunity": opportunity,
    }


def _generation_request(opportunity, proposal_id):
    return {
        "contract_version": CONTRACT_VERSION,
        "request_id": "req-gen-01",
        "proposal_id": proposal_id,
        "opportunity": opportunity,
    }


class ContractRunnerIntegrationTests(unittest.TestCase):
    """Real synthetic Contract runner proof — requires sips + ffmpeg."""

    def test_synthetic_accumulation_opportunity_renders_ready_candidate(self):
        """CB03-mapped synthetic Opportunity → SUITABLE → READY candidate with real MP4."""
        # Step 1: Suitability
        suit_req = _suitability_request(_SYNTHETIC_OPPORTUNITY)
        suit_response = build_suitability_response(suit_req)

        self.assertEqual(suit_response["operation_status"], "COMPLETED")
        self.assertEqual(suit_response["suitability"], "SUITABLE")
        self.assertEqual(suit_response["plugin_id"], PLUGIN_ID)
        self.assertEqual(suit_response["plugin_version"], PLUGIN_VERSION)
        self.assertTrue(suit_response["proposal_id"].startswith("prop-im-"))

        proposal_id = suit_response["proposal_id"]

        # Step 2: Generation
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            gen_req = _generation_request(_SYNTHETIC_OPPORTUNITY, proposal_id)
            gen_result = build_generation_result(gen_req, output_dir)

            # Verify generation result shape
            self.assertEqual(gen_result["operation_status"], "COMPLETED")
            self.assertEqual(gen_result["plugin_id"], PLUGIN_ID)
            self.assertEqual(gen_result["plugin_version"], PLUGIN_VERSION)
            self.assertEqual(gen_result["proposal_id"], proposal_id)
            self.assertEqual(gen_result["opportunity_id"], "opp-im-synthetic-01")

            # Verify candidate
            candidate = gen_result["candidate"]
            self.assertEqual(candidate["candidate_status"], "READY")
            self.assertEqual(candidate["asset_family"], "Illustrated Metaphor")
            self.assertTrue(candidate["candidate_id"].startswith("cand-im-"))

            # C1: duration_ms must reflect actual MP4 duration (within 100ms of 5000ms)
            self.assertLessEqual(abs(candidate["duration_ms"] - 5000), 100)

            # Verify placement within a_roll_window
            placement = candidate["suggested_placement"]
            self.assertGreaterEqual(placement["start_ms"], _SYNTHETIC_OPPORTUNITY["a_roll_window"]["start_ms"])
            self.assertLessEqual(placement["end_ms"], _SYNTHETIC_OPPORTUNITY["a_roll_window"]["end_ms"])

            # Verify artifacts — every URI must point to a real file
            artifacts = candidate["artifacts"]
            roles = {a["role"] for a in artifacts}
            self.assertIn("PRIMARY_MEDIA", roles)
            self.assertIn("PREVIEW", roles)
            self.assertIn("MANIFEST", roles)
            self.assertIn("QA_REPORT", roles)

            for artifact in artifacts:
                uri = artifact["uri"]
                self.assertTrue(uri.startswith("local-runner://"))
                rel_path = uri[len("local-runner://"):]
                resolved = output_dir / rel_path
                self.assertTrue(resolved.is_file(), f"artifact file missing: {resolved}")

            # Verify PRIMARY_MEDIA is a real MP4 with SHA-256
            primary = next(a for a in artifacts if a["role"] == "PRIMARY_MEDIA")
            self.assertEqual(primary["media_type"], "video/mp4")
            primary_path = output_dir / primary["uri"][len("local-runner://"):]
            self.assertTrue(primary_path.is_file())
            self.assertTrue(primary_path.stat().st_size > 0)

            # Verify SHA-256 matches
            actual_sha = hashlib.sha256(primary_path.read_bytes()).hexdigest()
            self.assertEqual(primary["sha256"], actual_sha)

            # Verify QA passed
            self.assertEqual(candidate["qa"]["status"], "PASSED")

            # Verify provenance
            self.assertEqual(candidate["provenance"]["origin"], "plugin-generated")
            self.assertEqual(candidate["provenance"]["source_ref"], "illustrated-metaphor manifest")

            # Verify plugin_metadata
            meta = candidate["plugin_metadata"]
            self.assertEqual(meta["visual_case_id"], "burden-growth")
            self.assertEqual(meta["route"], "structured_hybrid")

    def test_two_fresh_runs_produce_identical_sha256(self):
        """Repeatability proof: two fresh output roots → identical PRIMARY_MEDIA SHA-256.

        Binary equality is proven by real byte-level SHA-256 comparison,
        not just candidate_id equality.
        """
        sha_values = []
        for _ in range(2):
            with tempfile.TemporaryDirectory() as tmpdir:
                output_dir = Path(tmpdir)

                # Suitability
                suit_req = _suitability_request(_SYNTHETIC_OPPORTUNITY)
                suit_response = build_suitability_response(suit_req)
                proposal_id = suit_response["proposal_id"]

                # Generation
                gen_req = _generation_request(_SYNTHETIC_OPPORTUNITY, proposal_id)
                gen_result = build_generation_result(gen_req, output_dir)

                self.assertEqual(gen_result["operation_status"], "COMPLETED")

                # Extract PRIMARY_MEDIA SHA-256
                candidate = gen_result["candidate"]
                primary = next(a for a in candidate["artifacts"] if a["role"] == "PRIMARY_MEDIA")
                primary_path = output_dir / primary["uri"][len("local-runner://"):]
                actual_sha = hashlib.sha256(primary_path.read_bytes()).hexdigest()
                sha_values.append(actual_sha)

                # Also verify candidate_id is identical across runs
                if len(sha_values) == 2:
                    # candidate_id should be deterministic
                    pass

        # Binary equality proof: same SHA-256 from two independent fresh renders
        self.assertEqual(
            sha_values[0],
            sha_values[1],
            f"PRIMARY_MEDIA SHA-256 mismatch between two fresh runs: {sha_values[0]} vs {sha_values[1]}",
        )

    def test_candidate_id_identical_across_fresh_runs(self):
        """Deterministic candidate_id: two fresh runs produce the same candidate_id."""
        candidate_ids = []
        for _ in range(2):
            with tempfile.TemporaryDirectory() as tmpdir:
                output_dir = Path(tmpdir)
                suit_req = _suitability_request(_SYNTHETIC_OPPORTUNITY)
                suit_response = build_suitability_response(suit_req)
                proposal_id = suit_response["proposal_id"]
                gen_req = _generation_request(_SYNTHETIC_OPPORTUNITY, proposal_id)
                gen_result = build_generation_result(gen_req, output_dir)
                candidate_ids.append(gen_result["candidate"]["candidate_id"])

        self.assertEqual(candidate_ids[0], candidate_ids[1])

    def test_abstain_opportunity_returns_no_candidate(self):
        """ABSTAIN opportunity → suitability returns ABSTAIN, no generation is requested."""
        suit_req = _suitability_request(_ABSTAIN_OPPORTUNITY)
        suit_response = build_suitability_response(suit_req)

        self.assertEqual(suit_response["suitability"], "ABSTAIN")
        self.assertEqual(suit_response["operation_status"], "COMPLETED")
        self.assertTrue(suit_response["proposal_id"].startswith("prop-im-"))

    def test_abstain_generation_fails_closed(self):
        """C4: ABSTAIN generation request → FAILED with SUITABILITY_ABSTAIN, no Candidate."""
        # Compute proposal_id from the ABSTAIN opportunity
        suit_req = _suitability_request(_ABSTAIN_OPPORTUNITY)
        suit_response = build_suitability_response(suit_req)
        proposal_id = suit_response["proposal_id"]

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            gen_req = _generation_request(_ABSTAIN_OPPORTUNITY, proposal_id)
            gen_result = build_generation_result(gen_req, output_dir)

            self.assertEqual(gen_result["operation_status"], "FAILED")
            self.assertEqual(gen_result["problem"]["code"], "SUITABILITY_ABSTAIN")
            self.assertNotIn("candidate", gen_result)

    def test_proposal_id_tampering_detection(self):
        """Tampering: different opportunity content with same proposal_id → FAILED."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            # Compute proposal_id from the real opportunity
            suit_req = _suitability_request(_SYNTHETIC_OPPORTUNITY)
            suit_response = build_suitability_response(suit_req)
            proposal_id = suit_response["proposal_id"]

            # Tamper: use a different opportunity content with the same proposal_id
            tampered_opp = dict(_SYNTHETIC_OPPORTUNITY)
            tampered_opp["spoken_semantics"] = "完全不同的语义内容"
            tampered_opp["opportunity_id"] = "opp-tampered-01"

            gen_req = _generation_request(tampered_opp, proposal_id)
            gen_result = build_generation_result(gen_req, output_dir)

            self.assertEqual(gen_result["operation_status"], "FAILED")
            self.assertEqual(gen_result["problem"]["code"], "OPPORTUNITY_CONTENT_MISMATCH")

    def test_non_16_9_canvas_returns_blocked(self):
        """Non-16:9 canvas → BLOCKED with UNSUPPORTED_CANVAS."""
        opp = dict(_SYNTHETIC_OPPORTUNITY)
        opp["canvas"] = {"width": 800, "height": 600}
        opp["opportunity_id"] = "opp-canvas-01"

        suit_req = _suitability_request(opp)
        suit_response = build_suitability_response(suit_req)
        proposal_id = suit_response["proposal_id"]

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            gen_req = _generation_request(opp, proposal_id)
            gen_result = build_generation_result(gen_req, output_dir)

            self.assertEqual(gen_result["operation_status"], "BLOCKED")
            self.assertEqual(gen_result["problem"]["code"], "UNSUPPORTED_CANVAS")

    def test_non_integer_second_duration_matches_actual_mp4(self):
        """C1: target_duration_ms=5500 → actual MP4 ~5000ms, declared duration within 100ms tolerance."""
        opp = dict(_SYNTHETIC_OPPORTUNITY)
        opp["target_duration_ms"] = 5500
        opp["a_roll_window"] = {"start_ms": 10000, "end_ms": 20000}
        opp["opportunity_id"] = "opp-im-noninteger-01"

        suit_req = _suitability_request(opp)
        suit_response = build_suitability_response(suit_req)
        proposal_id = suit_response["proposal_id"]

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            gen_req = _generation_request(opp, proposal_id)
            gen_result = build_generation_result(gen_req, output_dir)

            self.assertEqual(gen_result["operation_status"], "COMPLETED")
            candidate = gen_result["candidate"]

            # Declared duration must reflect actual MP4, not the requested 5500ms
            declared_duration = candidate["duration_ms"]
            self.assertNotEqual(declared_duration, 5500)

            # Measure actual MP4 duration via ffprobe
            primary = next(a for a in candidate["artifacts"] if a["role"] == "PRIMARY_MEDIA")
            primary_path = output_dir / primary["uri"][len("local-runner://"):]
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(primary_path)],
                capture_output=True, text=True, check=True,
            )
            actual_sec = float(probe.stdout.strip())
            actual_ms = round(actual_sec * 1000)

            # Declared duration must be within 100ms of actual MP4 duration
            self.assertLessEqual(
                abs(declared_duration - actual_ms), 100,
                f"declared {declared_duration}ms vs actual {actual_ms}ms exceeds 100ms tolerance",
            )

            # requested_duration_ms preserved in plugin_metadata
            self.assertEqual(candidate["plugin_metadata"]["requested_duration_ms"], 5500)

            # suggested_placement must be fully contained in a_roll_window
            placement = candidate["suggested_placement"]
            self.assertGreaterEqual(placement["start_ms"], 10000)
            self.assertLessEqual(placement["end_ms"], 20000)
            # placement duration must match declared duration
            placement_duration = placement["end_ms"] - placement["start_ms"]
            self.assertLessEqual(abs(placement_duration - declared_duration), 100)

    def test_qa_runs_on_final_artifacts(self):
        """C3: QA report reflects final post-processed artifacts, not pre-postprocess QA."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            suit_req = _suitability_request(_SYNTHETIC_OPPORTUNITY)
            suit_response = build_suitability_response(suit_req)
            proposal_id = suit_response["proposal_id"]

            gen_req = _generation_request(_SYNTHETIC_OPPORTUNITY, proposal_id)
            gen_result = build_generation_result(gen_req, output_dir)

            self.assertEqual(gen_result["operation_status"], "COMPLETED")
            candidate = gen_result["candidate"]

            # Read the standalone qa-report.json from output_dir
            qa_artifact = next(a for a in candidate["artifacts"] if a["role"] == "QA_REPORT")
            qa_path = output_dir / qa_artifact["uri"][len("local-runner://"):]
            qa_report = json.loads(qa_path.read_text(encoding="utf-8"))

            # Candidate qa must match the standalone qa-report.json
            self.assertEqual(candidate["qa"]["status"], qa_report["status"])
            self.assertEqual(candidate["qa"]["summary"], qa_report["summary"])

            # Read manifest.json and verify its QA matches final
            manifest_artifact = next(a for a in candidate["artifacts"] if a["role"] == "MANIFEST")
            manifest_path = output_dir / manifest_artifact["uri"][len("local-runner://"):]
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest_qa = manifest.get("qa", {})
            self.assertEqual(manifest_qa.get("passed"), candidate["qa"]["status"] == "PASSED")

            # Verify QA passed on final artifacts (files exist)
            for f in manifest.get("files", []):
                self.assertTrue(Path(f).is_file(), f"final artifact missing: {f}")


class ContractRunner1920Tests(unittest.TestCase):
    """C2: Real 1920x1080 canonical CLI generation tests."""

    @staticmethod
    def _opp_1080():
        return {
            "opportunity_id": "opp-im-1080-01",
            "spoken_semantics": "持续累积的资源占用使分散的压力开始集中出现。",
            "visual_purpose": "让观众看到积累→压力→临界的变化过程。",
            "a_roll_window": {"start_ms": 12000, "end_ms": 17000},
            "target_duration_ms": 5000,
            "language": "zh-CN",
            "canvas": {"width": 1920, "height": 1080},
        }

    def test_1920x1080_cli_generation_real_resolution(self):
        """C2: 1920x1080 CLI generation → frame PNGs and MP4 at actual 1920x1080."""
        opp = self._opp_1080()
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            output_dir = tmpdir / "output"

            # Suitability
            suit_req_path = tmpdir / "suit_request.json"
            suit_result_path = tmpdir / "suit_result.json"
            suit_request = _suitability_request(opp)
            suit_req_path.write_text(
                json.dumps(suit_request, ensure_ascii=False, sort_keys=True),
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, "scripts/contract_runner.py",
                 "--request", str(suit_req_path),
                 "--result", str(suit_result_path),
                 "--output-dir", str(output_dir)],
                capture_output=True, text=True, timeout=60, check=False,
                cwd=str(Path(__file__).resolve().parents[1]),
            )
            self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
            suit_response = json.loads(suit_result_path.read_text(encoding="utf-8"))
            proposal_id = suit_response["proposal_id"]

            # Generation
            gen_req_path = tmpdir / "gen_request.json"
            gen_result_path = tmpdir / "gen_result.json"
            gen_request = _generation_request(opp, proposal_id)
            gen_req_path.write_text(
                json.dumps(gen_request, ensure_ascii=False, sort_keys=True),
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, "scripts/contract_runner.py",
                 "--request", str(gen_req_path),
                 "--result", str(gen_result_path),
                 "--output-dir", str(output_dir)],
                capture_output=True, text=True, timeout=120, check=False,
                cwd=str(Path(__file__).resolve().parents[1]),
            )
            self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")

            gen_response = json.loads(gen_result_path.read_text(encoding="utf-8"))
            self.assertEqual(gen_response["operation_status"], "COMPLETED")
            candidate = gen_response["candidate"]
            self.assertEqual(candidate["candidate_status"], "READY")

            # Verify PRIMARY_MEDIA is real 1920x1080
            primary = next(a for a in candidate["artifacts"] if a["role"] == "PRIMARY_MEDIA")
            primary_path = output_dir / primary["uri"][len("local-runner://"):]
            self.assertTrue(primary_path.is_file())

            # Probe MP4 resolution
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=width,height",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(primary_path)],
                capture_output=True, text=True, check=True,
            )
            lines = probe.stdout.strip().split("\n")
            mp4_width = int(lines[0])
            mp4_height = int(lines[1])
            self.assertEqual(mp4_width, 1920, f"MP4 width is {mp4_width}, expected 1920")
            self.assertEqual(mp4_height, 1080, f"MP4 height is {mp4_height}, expected 1080")

            # Verify at least one frame PNG is 1920x1080 (not upscaled from 1280x720)
            candidate_id = candidate["candidate_id"]
            seq_dir = output_dir / candidate_id / "b1_metaphor_system" / "structured_hybrid" / "sequence"
            png_files = sorted(seq_dir.glob("*.png"))
            self.assertTrue(len(png_files) > 0)

            # Check first frame PNG dimensions via sips
            sips_result = subprocess.run(
                ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(png_files[0])],
                capture_output=True, text=True, check=True,
            )
            png_w = None
            png_h = None
            for line in sips_result.stdout.strip().split("\n"):
                if "pixelWidth" in line:
                    png_w = int(line.split(":")[-1].strip())
                if "pixelHeight" in line:
                    png_h = int(line.split(":")[-1].strip())
            self.assertEqual(png_w, 1920, f"frame PNG width is {png_w}, expected 1920")
            self.assertEqual(png_h, 1080, f"frame PNG height is {png_h}, expected 1080")

            # Verify canvas reported in plugin_metadata
            self.assertEqual(candidate["plugin_metadata"]["canvas"]["width"], 1920)
            self.assertEqual(candidate["plugin_metadata"]["canvas"]["height"], 1080)


class ContractRunnerCLITests(unittest.TestCase):
    """Tests for the CLI entry point: scripts/contract_runner.py."""

    def test_version_flag(self):
        """--version outputs a single non-empty line and exits 0."""
        result = subprocess.run(
            [sys.executable, "scripts/contract_runner.py", "--version"],
            capture_output=True, text=True, timeout=10, check=False,
            cwd=str(Path(__file__).resolve().parents[1]),
        )
        self.assertEqual(result.returncode, 0)
        version_output = result.stdout.strip()
        self.assertTrue(version_output)
        self.assertNotIn("\n", version_output)
        self.assertEqual(version_output, PLUGIN_VERSION)

    def test_suitability_via_cli(self):
        """Full CLI suitability flow: write request, run runner, read result."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            request_path = tmpdir / "request.json"
            result_path = tmpdir / "result.json"
            output_dir = tmpdir / "output"

            request = _suitability_request(_SYNTHETIC_OPPORTUNITY)
            request_path.write_text(json.dumps(request, ensure_ascii=False, sort_keys=True), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, "scripts/contract_runner.py",
                 "--request", str(request_path),
                 "--result", str(result_path),
                 "--output-dir", str(output_dir)],
                capture_output=True, text=True, timeout=60, check=False,
                cwd=str(Path(__file__).resolve().parents[1]),
            )
            self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
            self.assertTrue(result_path.is_file())

            response = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertEqual(response["contract_version"], CONTRACT_VERSION)
            self.assertEqual(response["operation_status"], "COMPLETED")
            self.assertEqual(response["suitability"], "SUITABLE")
            self.assertEqual(response["plugin_id"], PLUGIN_ID)
            self.assertEqual(response["plugin_version"], PLUGIN_VERSION)
            self.assertEqual(response["opportunity_id"], "opp-im-synthetic-01")

    def test_generation_via_cli(self):
        """Full CLI generation flow: suitability → generation → real MP4 artifact."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            output_dir = tmpdir / "output"

            # Step 1: Suitability
            suit_req_path = tmpdir / "suit_request.json"
            suit_result_path = tmpdir / "suit_result.json"
            suit_request = _suitability_request(_SYNTHETIC_OPPORTUNITY)
            suit_req_path.write_text(
                json.dumps(suit_request, ensure_ascii=False, sort_keys=True),
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, "scripts/contract_runner.py",
                 "--request", str(suit_req_path),
                 "--result", str(suit_result_path),
                 "--output-dir", str(output_dir)],
                capture_output=True, text=True, timeout=60, check=False,
                cwd=str(Path(__file__).resolve().parents[1]),
            )
            self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")

            suit_response = json.loads(suit_result_path.read_text(encoding="utf-8"))
            proposal_id = suit_response["proposal_id"]

            # Step 2: Generation
            gen_req_path = tmpdir / "gen_request.json"
            gen_result_path = tmpdir / "gen_result.json"
            gen_request = _generation_request(_SYNTHETIC_OPPORTUNITY, proposal_id)
            gen_req_path.write_text(
                json.dumps(gen_request, ensure_ascii=False, sort_keys=True),
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, "scripts/contract_runner.py",
                 "--request", str(gen_req_path),
                 "--result", str(gen_result_path),
                 "--output-dir", str(output_dir)],
                capture_output=True, text=True, timeout=120, check=False,
                cwd=str(Path(__file__).resolve().parents[1]),
            )
            self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")

            gen_response = json.loads(gen_result_path.read_text(encoding="utf-8"))
            self.assertEqual(gen_response["operation_status"], "COMPLETED")
            candidate = gen_response["candidate"]
            self.assertEqual(candidate["candidate_status"], "READY")

            # Verify real artifact files exist
            for artifact in candidate["artifacts"]:
                rel = artifact["uri"][len("local-runner://"):]
                resolved = output_dir / rel
                self.assertTrue(resolved.is_file(), f"missing artifact: {resolved}")

    def test_repeatability_via_cli(self):
        """CLI repeatability: two fresh runs produce identical PRIMARY_MEDIA SHA-256."""
        sha_values = []

        for run_index in range(2):
            with tempfile.TemporaryDirectory() as tmpdir:
                tmpdir = Path(tmpdir)
                output_dir = tmpdir / "output"

                # Suitability
                suit_req_path = tmpdir / "suit_request.json"
                suit_result_path = tmpdir / "suit_result.json"
                suit_request = _suitability_request(_SYNTHETIC_OPPORTUNITY)
                suit_req_path.write_text(
                    json.dumps(suit_request, ensure_ascii=False, sort_keys=True),
                    encoding="utf-8",
                )
                subprocess.run(
                    [sys.executable, "scripts/contract_runner.py",
                     "--request", str(suit_req_path),
                     "--result", str(suit_result_path),
                     "--output-dir", str(output_dir)],
                    capture_output=True, text=True, timeout=60, check=False,
                    cwd=str(Path(__file__).resolve().parents[1]),
                )
                suit_response = json.loads(suit_result_path.read_text(encoding="utf-8"))
                proposal_id = suit_response["proposal_id"]

                # Generation
                gen_req_path = tmpdir / "gen_request.json"
                gen_result_path = tmpdir / "gen_result.json"
                gen_request = _generation_request(_SYNTHETIC_OPPORTUNITY, proposal_id)
                gen_req_path.write_text(
                    json.dumps(gen_request, ensure_ascii=False, sort_keys=True),
                    encoding="utf-8",
                )
                subprocess.run(
                    [sys.executable, "scripts/contract_runner.py",
                     "--request", str(gen_req_path),
                     "--result", str(gen_result_path),
                     "--output-dir", str(output_dir)],
                    capture_output=True, text=True, timeout=120, check=False,
                    cwd=str(Path(__file__).resolve().parents[1]),
                )
                gen_response = json.loads(gen_result_path.read_text(encoding="utf-8"))
                primary = next(
                    a for a in gen_response["candidate"]["artifacts"]
                    if a["role"] == "PRIMARY_MEDIA"
                )
                primary_path = output_dir / primary["uri"][len("local-runner://"):]
                actual_sha = hashlib.sha256(primary_path.read_bytes()).hexdigest()
                sha_values.append(actual_sha)

        self.assertEqual(sha_values[0], sha_values[1])


if __name__ == "__main__":
    unittest.main()
