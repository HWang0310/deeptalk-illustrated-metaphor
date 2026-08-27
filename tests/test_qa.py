import unittest

from illustrated_metaphor.qa import run_qa


class QATests(unittest.TestCase):
    def test_reference_asset_requires_provenance_note(self):
        report = run_qa({"track": "a_reference", "duration_seconds": 5, "files": []})

        self.assertFalse(report["passed"])
        self.assertIn("Track A requires upstream-reference provenance", report["failures"])

