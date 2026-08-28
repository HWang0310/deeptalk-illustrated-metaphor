import tempfile
import unittest
from pathlib import Path

from illustrated_metaphor.cli import render_prototypes, render_v01_comparison, render_v02_comparison


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
