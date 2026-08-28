import tempfile
import unittest
from pathlib import Path

from illustrated_metaphor.cli import render_common_brief_trial, render_prototypes, render_v01_comparison, render_v02_comparison


class CliTests(unittest.TestCase):
    def test_render_creates_asset_manifest_for_both_tracks(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            manifest = render_prototypes(Path(temporary_directory), case_limit=1)

        self.assertEqual({"a_reference", "b_neutral"}, {asset["track"] for asset in manifest["assets"]})
        self.assertEqual(6, len(manifest["assets"]))

    def test_v01_comparison_renders_35_comparable_assets(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            manifest = render_v01_comparison(Path(temporary_directory))

        self.assertEqual(35, len(manifest["assets"]))
        self.assertEqual(
            {"a_reference", "b_neutral", "b_paper_relay", "b_object_theatre"},
            {asset["track"] for asset in manifest["assets"]},
        )
        self.assertEqual(7, sum(asset["route"] == "structured_hybrid" for asset in manifest["assets"]))

    def test_v02_comparison_renders_four_baselines_and_three_selective_state_studies(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            manifest = render_v02_comparison(Path(temporary_directory))

        self.assertEqual(31, len(manifest["assets"]))
        self.assertEqual(
            {"a_reference", "b_paper_relay", "b1_metaphor_system", "b_object_theatre"},
            {asset["track"] for asset in manifest["assets"]},
        )
        self.assertEqual(3, sum(asset["route"] == "structured_hybrid" for asset in manifest["assets"]))
        system_assets = [asset for asset in manifest["assets"] if asset["track"] == "b1_metaphor_system"]
        self.assertTrue(all(asset["qa"]["passed"] for asset in system_assets))

    def test_v02_approved_still_uses_final_readable_scene_state(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            manifest = render_v02_comparison(Path(temporary_directory))
            fragility = next(
                asset for asset in manifest["assets"]
                if asset["case_id"] == "hidden-fragility"
                and asset["track"] == "b1_metaphor_system"
                and asset["route"] == "approved_still"
            )
            svg = Path(fragility["files"][2]).with_suffix(".svg").read_text(encoding="utf-8")

        self.assertIn("hidden-fragility · state 2", svg)
        self.assertIn('stroke="#ef7350"', svg)

    def test_common_brief_trial_renders_seven_b1_candidates_and_records_the_abstention(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            manifest = render_common_brief_trial(Path(temporary_directory))
            cb03 = next(asset for asset in manifest["assets"] if asset["case_id"] == "CB03")
            source_svg = Path(cb03["files"][-1]).with_suffix(".svg").read_text(encoding="utf-8")

        self.assertEqual("common-brief-trial", manifest["study"])
        self.assertEqual(7, len(manifest["assets"]))
        self.assertEqual(["CB08"], [item["id"] for item in manifest["abstentions"]])
        self.assertEqual({"b1_metaphor_system"}, {asset["track"] for asset in manifest["assets"]})
        self.assertEqual("burden-growth", cb03["visual_case_id"])
        self.assertEqual("CB03", cb03["case_id"])
        self.assertIn("CB03 · state 3", source_svg)
        self.assertTrue(all(asset["qa"]["passed"] for asset in manifest["assets"]))
