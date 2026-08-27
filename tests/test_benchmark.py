import unittest

from illustrated_metaphor.benchmark import load_cases


class BenchmarkTests(unittest.TestCase):
    def test_v0_cases_have_unique_ids_and_required_fields(self):
        cases = load_cases("benchmarks/v0-cases.json")

        self.assertGreaterEqual(len(cases), 7)
        self.assertEqual({case["id"] for case in cases}.__len__(), len(cases))
        for case in cases:
            self.assertEqual({"a_reference", "b_neutral"}, set(case["tracks"]))
            for field in ("semantic_intent", "metaphor", "scene_states", "text", "duration_seconds", "qa_criteria"):
                self.assertIn(field, case)

