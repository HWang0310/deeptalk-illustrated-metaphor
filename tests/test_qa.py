import unittest

from illustrated_metaphor.qa import run_qa


class QATests(unittest.TestCase):
    def test_reference_asset_requires_provenance_note(self):
        report = run_qa({"track": "a_reference", "duration_seconds": 5, "files": []})

        self.assertFalse(report["passed"])
        self.assertIn("Track A requires upstream-reference provenance", report["failures"])

    def test_original_candidate_requires_explicit_hypothesis_provenance(self):
        report = run_qa({"track": "b_paper_relay", "duration_seconds": 5, "files": [], "state_names": ["start"]})

        self.assertFalse(report["passed"])
        self.assertIn("Track B candidate requires original-language provenance", report["failures"])

    def test_v02_system_requires_structural_readability_metadata(self):
        report = run_qa({
            "track": "b1_metaphor_system",
            "provenance": "original-metaphor-system",
            "duration_seconds": 5,
            "files": [],
            "state_names": ["start", "end"],
            "visual_qa": {"object_count": 2, "annotation_count": 1, "actor_object_separation": True, "clutter_candidate": False, "final_frame_readability": "candidate"},
        })

        self.assertFalse(report["passed"])
        self.assertIn("V0.2 system requires a focal object", report["failures"])

    def test_common_brief_candidate_requires_full_trial_review_metadata(self):
        report = run_qa({
            "study": "common-brief-trial",
            "track": "b1_metaphor_system",
            "provenance": "original-metaphor-system",
            "duration_seconds": 5,
            "files": [],
            "state_names": ["start", "end"],
            "visual_qa": {"focal_object": "load", "object_count": 2, "annotation_count": 1, "uses_actor": True, "actor_object_separation": True, "clutter_candidate": False, "final_frame_readability": "candidate"},
        })

        self.assertFalse(report["passed"])
        self.assertIn("Common Brief trial requires a complete review rubric", report["failures"])
