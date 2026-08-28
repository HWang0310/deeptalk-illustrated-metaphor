import unittest

from illustrated_metaphor.vocabulary import CASE_IDS, get_metaphor_spec, render_b1_system


class VocabularyTests(unittest.TestCase):
    def test_all_benchmark_cases_have_distinct_original_v02_specs(self):
        specs = [get_metaphor_spec(case_id) for case_id in CASE_IDS]

        self.assertEqual(7, len(specs))
        self.assertEqual(7, len({spec.metaphor for spec in specs}))
        self.assertEqual(7, len({spec.focal_object for spec in specs}))
        self.assertTrue(all(spec.annotation_position == "upper-left" for spec in specs))
        self.assertTrue(all(1 <= len(spec.objects) <= 4 for spec in specs))

    def test_paper_relay_grammar_preserves_generic_actor_and_allows_object_only_network(self):
        burden = get_metaphor_spec("burden-growth")
        network = get_metaphor_spec("network-effect")

        self.assertEqual("bearer", burden.actor_role)
        self.assertIn("load", burden.objects)
        self.assertIsNone(network.actor_role)
        self.assertIn("network-node", network.objects)

    def test_renderer_marks_focal_objects_and_actor_object_separation(self):
        burden_svg = render_b1_system("burden-growth", 1)
        network_svg = render_b1_system("network-effect", 1)

        self.assertIn('data-metaphor="burden"', burden_svg)
        self.assertIn('data-focal-object="load"', burden_svg)
        self.assertIn('data-role="actor"', burden_svg)
        self.assertIn('data-role="object"', burden_svg)
        self.assertNotIn('data-role="actor"', network_svg)
        self.assertIn('data-focal-object="origin-node"', network_svg)

