"""Unit tests for Contract V1 pure functions (no rendering, no subprocess)."""

import unittest

from illustrated_metaphor.contract import (
    ASSET_FAMILY,
    CONTRACT_VERSION,
    PLUGIN_ID,
    PLUGIN_VERSION,
    _canonical_json,
    _clamp_duration,
    _derive_candidate_text,
    _is_canvas_supported,
    _opportunity_content_digest,
    _resolve_canvas,
    _sha256_hex,
    assess_suitability,
    build_suitability_response,
    compute_candidate_id,
    compute_proposal_id,
    map_opportunity_to_case,
)


def _opportunity(
    semantics="持续累积的资源占用使分散的压力开始集中出现。",
    purpose="让观众看到积累→压力→临界的变化过程。",
    duration_ms=5000,
    canvas_width=1920,
    canvas_height=1080,
    opportunity_id="opp-test-01",
):
    return {
        "opportunity_id": opportunity_id,
        "spoken_semantics": semantics,
        "visual_purpose": purpose,
        "a_roll_window": {"start_ms": 12000, "end_ms": 17000},
        "target_duration_ms": duration_ms,
        "language": "zh-CN",
        "canvas": {"width": canvas_width, "height": canvas_height},
    }


def _request(opportunity=None, proposal_id=None):
    req = {
        "contract_version": "visual-asset-plugin-contract/1",
        "request_id": "req-test-01",
        "opportunity": opportunity or _opportunity(),
    }
    if proposal_id is not None:
        req["proposal_id"] = proposal_id
    return req


class SuitabilityTests(unittest.TestCase):
    def test_suitable_for_accumulation(self):
        opp = _opportunity(semantics="每一轮扩张都会增加新的承诺和资源占用，直到原本分散的压力开始集中出现。")
        suitability, reason, _case_id = assess_suitability(opp)
        self.assertEqual(suitability, "SUITABLE")
        self.assertIn("压力", reason)

    def test_suitable_for_feedback_loop(self):
        opp = _opportunity(semantics="体验改善带来用户增长，更多用户产生更多数据，数据又帮助产品继续改善。")
        suitability, _reason, _case_id = assess_suitability(opp)
        self.assertEqual(suitability, "SUITABLE")

    def test_suitable_for_tension(self):
        opp = _opportunity(semantics="增长团队希望扩大规模，财务团队希望控制风险，资源分配因此形成持续拉扯。")
        suitability, _reason, _case_id = assess_suitability(opp)
        self.assertEqual(suitability, "SUITABLE")

    def test_suitable_for_surface_vs_mechanism(self):
        opp = _opportunity(semantics="表面看起来稳定，可能只是压力被暂时转移，并不意味着底层风险已经消失。")
        suitability, _reason, _case_id = assess_suitability(opp)
        self.assertEqual(suitability, "SUITABLE")

    def test_borderline_for_core_judgment(self):
        opp = _opportunity(
            semantics="真正的问题不是增长快，而是增长是否依赖下一轮增长才能维持。",
            purpose="让观众快速理解一个核心判断。",
        )
        suitability, _reason, _case_id = assess_suitability(opp)
        self.assertEqual(suitability, "BORDERLINE")

    def test_borderline_for_causal_chain(self):
        opp = _opportunity(
            semantics="成本上升，先压缩利润；利润收窄后投入下降，最后才反映到用户体验。",
            purpose="表达 cause → transmission → consequence 的因果链。",
        )
        suitability, _reason, _case_id = assess_suitability(opp)
        self.assertEqual(suitability, "BORDERLINE")

    def test_borderline_for_rule_change(self):
        opp = _opportunity(
            semantics="规则改变以前有效的路径，在规则改变以后，可能会产生完全不同的结果。",
            purpose="表达 before → rule change → after。",
        )
        suitability, _reason, _case_id = assess_suitability(opp)
        self.assertEqual(suitability, "BORDERLINE")

    def test_abstain_for_numeric_evidence(self):
        opp = _opportunity(
            semantics="用户留存率从 42% 提升到 58%，真正重要的不是数字变大。",
            purpose="表达 42% → 58% 的数据变化。",
        )
        suitability, _reason, _case_id = assess_suitability(opp)
        self.assertEqual(suitability, "ABSTAIN")

    def test_abstain_for_percentage(self):
        opp = _opportunity(semantics="环比增长 15%，百分比变化显著。")
        suitability, _reason, _case_id = assess_suitability(opp)
        self.assertEqual(suitability, "ABSTAIN")

    def test_abstain_proposal_id_exists_but_no_case_mapping(self):
        opp = _opportunity(semantics="环比增长 15%，百分比变化显著。")
        suitability, _reason, case_id = assess_suitability(opp)
        self.assertEqual(suitability, "ABSTAIN")
        self.assertEqual(case_id, "")


class CaseMappingTests(unittest.TestCase):
    def test_case_mapping_for_pressure(self):
        opp = _opportunity(semantics="持续累积的压力")
        case_id, route = map_opportunity_to_case(opp)
        self.assertEqual(case_id, "burden-growth")
        self.assertEqual(route, "structured_hybrid")

    def test_case_mapping_for_tension(self):
        opp = _opportunity(semantics="两方拉扯同一根绳子")
        case_id, route = map_opportunity_to_case(opp)
        self.assertEqual(case_id, "tug-of-war")
        self.assertEqual(route, "approved_still")

    def test_case_mapping_for_feedback_loop(self):
        opp = _opportunity(semantics="反馈循环加速")
        case_id, _route = map_opportunity_to_case(opp)
        self.assertEqual(case_id, "speed-loop")

    def test_case_mapping_abstain_returns_empty(self):
        opp = _opportunity(semantics="精确数值变化")
        case_id, route = map_opportunity_to_case(opp)
        self.assertEqual(case_id, "")
        self.assertEqual(route, "none")


class ProposalIdTests(unittest.TestCase):
    def test_proposal_id_deterministic(self):
        opp = _opportunity()
        digest = _opportunity_content_digest(opp)
        pid1 = compute_proposal_id(PLUGIN_ID, PLUGIN_VERSION, digest, "SUITABLE", "burden-growth", "structured_hybrid")
        pid2 = compute_proposal_id(PLUGIN_ID, PLUGIN_VERSION, digest, "SUITABLE", "burden-growth", "structured_hybrid")
        self.assertEqual(pid1, pid2)
        self.assertTrue(pid1.startswith("prop-im-"))

    def test_proposal_id_changes_with_content(self):
        opp1 = _opportunity(semantics="积累压力")
        opp2 = _opportunity(semantics="反馈循环")
        d1 = _opportunity_content_digest(opp1)
        d2 = _opportunity_content_digest(opp2)
        pid1 = compute_proposal_id(PLUGIN_ID, PLUGIN_VERSION, d1, "SUITABLE", "burden-growth", "structured_hybrid")
        pid2 = compute_proposal_id(PLUGIN_ID, PLUGIN_VERSION, d2, "SUITABLE", "speed-loop", "structured_hybrid")
        self.assertNotEqual(pid1, pid2)

    def test_proposal_id_changes_with_plugin_version(self):
        opp = _opportunity()
        digest = _opportunity_content_digest(opp)
        pid1 = compute_proposal_id(PLUGIN_ID, "0.2.0", digest, "SUITABLE", "burden-growth", "structured_hybrid")
        pid2 = compute_proposal_id(PLUGIN_ID, "0.3.0", digest, "SUITABLE", "burden-growth", "structured_hybrid")
        self.assertNotEqual(pid1, pid2)


class CandidateIdTests(unittest.TestCase):
    def test_candidate_id_deterministic(self):
        cid1 = compute_candidate_id("prop-im-abc123", PLUGIN_VERSION, "scene-digest-xyz", "structured_hybrid", '{"canvas_width":1920}')
        cid2 = compute_candidate_id("prop-im-abc123", PLUGIN_VERSION, "scene-digest-xyz", "structured_hybrid", '{"canvas_width":1920}')
        self.assertEqual(cid1, cid2)
        self.assertTrue(cid1.startswith("cand-im-"))

    def test_candidate_id_changes_with_route(self):
        cid1 = compute_candidate_id("prop-im-abc123", PLUGIN_VERSION, "scene-digest-xyz", "structured_hybrid", "{}")
        cid2 = compute_candidate_id("prop-im-abc123", PLUGIN_VERSION, "scene-digest-xyz", "approved_still", "{}")
        self.assertNotEqual(cid1, cid2)

    def test_candidate_id_changes_with_render_settings(self):
        cid1 = compute_candidate_id("prop-im-abc123", PLUGIN_VERSION, "scene-digest-xyz", "structured_hybrid", '{"canvas_width":1280}')
        cid2 = compute_candidate_id("prop-im-abc123", PLUGIN_VERSION, "scene-digest-xyz", "structured_hybrid", '{"canvas_width":1920}')
        self.assertNotEqual(cid1, cid2)


class SuitabilityResponseTests(unittest.TestCase):
    def test_suitability_response_shape(self):
        req = _request()
        response = build_suitability_response(req)
        self.assertEqual(response["contract_version"], CONTRACT_VERSION)
        self.assertEqual(response["request_id"], "req-test-01")
        self.assertEqual(response["opportunity_id"], "opp-test-01")
        self.assertEqual(response["plugin_id"], PLUGIN_ID)
        self.assertEqual(response["plugin_version"], PLUGIN_VERSION)
        self.assertEqual(response["operation_status"], "COMPLETED")
        self.assertIn("proposal_id", response)
        self.assertIn("suitability", response)
        self.assertIn("reason", response)

    def test_suitability_response_correlation(self):
        opp = _opportunity(opportunity_id="opp-correlation-01")
        req = _request(opportunity=opp)
        response = build_suitability_response(req)
        self.assertEqual(response["opportunity_id"], "opp-correlation-01")
        self.assertEqual(response["request_id"], "req-test-01")

    def test_abstain_response_has_proposal_id(self):
        opp = _opportunity(semantics="精确数值和百分比变化")
        req = _request(opportunity=opp)
        response = build_suitability_response(req)
        self.assertEqual(response["suitability"], "ABSTAIN")
        self.assertTrue(response["proposal_id"].startswith("prop-im-"))

    def test_suitable_response_no_problem_field(self):
        req = _request()
        response = build_suitability_response(req)
        self.assertNotIn("problem", response)


class VersionTests(unittest.TestCase):
    def test_version_is_nonempty_string(self):
        self.assertIsInstance(PLUGIN_VERSION, str)
        self.assertTrue(PLUGIN_VERSION.strip())

    def test_version_single_line(self):
        self.assertNotIn("\n", PLUGIN_VERSION)


class CanvasTests(unittest.TestCase):
    def test_1280x720_native(self):
        opp = _opportunity(canvas_width=1280, canvas_height=720)
        w, h, _note = _resolve_canvas(opp)
        self.assertEqual(w, 1280)
        self.assertEqual(h, 720)
        self.assertTrue(_is_canvas_supported(opp))

    def test_1920x1080_supported(self):
        opp = _opportunity(canvas_width=1920, canvas_height=1080)
        self.assertTrue(_is_canvas_supported(opp))
        w, h, _note = _resolve_canvas(opp)
        self.assertEqual(w, 1920)
        self.assertEqual(h, 1080)

    def test_non_16_9_not_supported(self):
        opp = _opportunity(canvas_width=800, canvas_height=600)
        self.assertFalse(_is_canvas_supported(opp))


class DurationTests(unittest.TestCase):
    def test_clamp_to_minimum(self):
        self.assertEqual(_clamp_duration(1000), 3000)

    def test_clamp_to_maximum(self):
        self.assertEqual(_clamp_duration(20000), 10000)

    def test_clamp_within_range(self):
        self.assertEqual(_clamp_duration(5000), 5000)


class CandidateTextTests(unittest.TestCase):
    def test_first_clause_extraction(self):
        opp = _opportunity(semantics="每一轮扩张都会增加新的承诺，直到压力集中出现。")
        text = _derive_candidate_text(opp, "burden-growth")
        self.assertEqual(text, "每一轮扩张都会增加新的承诺")

    def test_truncation_when_no_clause(self):
        opp = _opportunity(semantics="短文本")
        text = _derive_candidate_text(opp, "burden-growth")
        self.assertEqual(text, "短文本")


class CanonicalJsonTests(unittest.TestCase):
    def test_canonical_json_sorted(self):
        result = _canonical_json({"b": 1, "a": 2})
        self.assertEqual(result, '{"a":2,"b":1}')

    def test_sha256_deterministic(self):
        self.assertEqual(_sha256_hex("test"), _sha256_hex("test"))


class ProvenanceTests(unittest.TestCase):
    def test_asset_family_identity(self):
        self.assertEqual(ASSET_FAMILY, "Illustrated Metaphor")

    def test_plugin_id_matches_core_config(self):
        self.assertEqual(PLUGIN_ID, "org.deeptalk.illustrated-metaphor")


if __name__ == "__main__":
    unittest.main()
