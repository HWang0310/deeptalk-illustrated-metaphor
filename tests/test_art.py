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

    def test_v01_candidates_separate_generic_actor_from_object_theatre(self):
        paper_relay_svg = render_svg(CASE, "b_paper_relay", 1)
        object_theatre_svg = render_svg(CASE, "b_object_theatre", 1)

        self.assertIn('data-provenance="original-language-hypothesis"', paper_relay_svg)
        self.assertIn('class="generic-paper-actor"', paper_relay_svg)
        self.assertIn('class="object-theatre"', object_theatre_svg)
        self.assertNotIn('class="generic-paper-actor"', object_theatre_svg)
        self.assertNotIn('class="black-figure"', object_theatre_svg)

    def test_primary_candidate_uses_distinct_metaphor_grammar_for_each_benchmark_case(self):
        cases = {
            "burden-growth": "burden",
            "tug-of-war": "tension",
            "speed-loop": "loop",
            "hidden-fragility": "fragility",
            "information-overload": "overload",
            "network-effect": "network",
            "state-transition": "transition",
        }
        for case_id, grammar in cases.items():
            svg = render_svg({**CASE, "id": case_id}, "b_paper_relay", 1)
            self.assertIn(f'data-metaphor="{grammar}"', svg)

    def test_paper_relay_keeps_actor_separate_from_case_specific_object(self):
        svg = render_svg({**CASE, "id": "speed-loop"}, "b_paper_relay", 1)

        self.assertNotIn('M645 510 L760 285 L850 510', svg)
        self.assertIn('data-metaphor="loop"', svg)
