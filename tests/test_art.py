import unittest

from illustrated_metaphor.art import render_svg


CASE = {
    "id": "burden-growth",
    "text": "负担越滚越大",
    "scene_states": [{"name": "start"}, {"name": "strain"}],
}


class ArtTests(unittest.TestCase):
    def test_tracks_have_distinct_language_and_preserve_chinese_annotation(self):
        reference_svg = render_svg(CASE, "a_reference", 1)
        neutral_svg = render_svg(CASE, "b_neutral", 1)

        self.assertIn('data-track="a_reference"', reference_svg)
        self.assertIn('data-provenance="upstream-reference-only"', reference_svg)
        self.assertIn('class="black-figure"', reference_svg)
        self.assertIn("负担越滚越大", reference_svg)
        self.assertIn('data-track="b_neutral"', neutral_svg)
        self.assertIn('class="paper-collage"', neutral_svg)
        self.assertIn('class="neutral-form"', neutral_svg)
        self.assertNotIn('class="black-figure"', neutral_svg)

