import tempfile
import unittest
from pathlib import Path

from illustrated_metaphor.cli import render_prototypes


class CliTests(unittest.TestCase):
    def test_render_creates_asset_manifest_for_both_tracks(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            manifest = render_prototypes(Path(temporary_directory), case_limit=1)

        self.assertEqual({"a_reference", "b_neutral"}, {asset["track"] for asset in manifest["assets"]})
        self.assertEqual(6, len(manifest["assets"]))

