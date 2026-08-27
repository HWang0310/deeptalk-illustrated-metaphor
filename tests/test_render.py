import tempfile
import unittest
from pathlib import Path

from illustrated_metaphor.render import render_frame


class RenderTests(unittest.TestCase):
    def test_frame_carries_case_id_into_svg_metaphor_grammar(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            png_path = Path(temporary_directory) / "frame.png"
            render_frame("b_paper_relay", "越转越快", 1, png_path, case_id="speed-loop")
            svg = png_path.with_suffix(".svg").read_text(encoding="utf-8")

        self.assertIn('data-metaphor="loop"', svg)
