import unittest

from illustrated_metaphor.common_briefs import load_common_briefs


class CommonBriefTests(unittest.TestCase):
    def test_trial_keeps_exact_eight_briefs_and_a_deliberate_numeric_abstention(self):
        briefs = load_common_briefs()

        self.assertEqual([f"CB{number:02d}" for number in range(1, 9)], [brief["id"] for brief in briefs])
        self.assertEqual("真正的问题不是增长快，而是增长是否依赖下一轮增长才能维持。", briefs[0]["spoken_semantics"])
        self.assertEqual("用户留存率从 42% 提升到 58%，真正重要的不是数字变大，而是首次完成路径被明显缩短。", briefs[-1]["spoken_semantics"])
        self.assertEqual(["CB08"], [brief["id"] for brief in briefs if brief["suitability"] == "ABSTAIN"])
        self.assertEqual(7, sum(brief["candidate"] for brief in briefs))

    def test_actual_candidates_remain_b1_and_do_not_create_track_a_trial_assets(self):
        candidates = [brief for brief in load_common_briefs() if brief["candidate"]]

        self.assertEqual({"b1_metaphor_system"}, {brief["track"] for brief in candidates})
        self.assertNotIn("a_reference", {brief["track"] for brief in candidates})
        self.assertTrue(all(brief["visual_case_id"] for brief in candidates))
        self.assertTrue(all(brief["route"] in {"approved_still", "structured_hybrid"} for brief in candidates))
