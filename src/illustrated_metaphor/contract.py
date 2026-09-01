"""Visual Asset Plugin Contract V1 pure functions for Illustrated Metaphor.

All functions are pure (no I/O) unless explicitly documented.
No Core imports, no network/service dependency, no fixture file lookup.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from .cli import _render_asset
from .vocabulary import get_metaphor_spec

# --- Constants --------------------------------------------------------------

PLUGIN_ID = "org.deeptalk.illustrated-metaphor"
PLUGIN_VERSION = "0.2.0-contract-runner"
CONTRACT_VERSION = "visual-asset-plugin-contract/1"
ASSET_FAMILY = "Illustrated Metaphor"

# --- Suitability keyword patterns -------------------------------------------

_ABSTAIN_KEYWORDS = (
    "留存率", "百分比", "%", "数据变化", "数值", "数字", "精确",
    "统计", "比率", "同比增长", "环比", "KPI", "指标数据",
)

_BORDERLINE_KEYWORDS = (
    "因果链", "因果", "条件判断", "业务判断", "核心判断",
    "规则改变", "规则变化", "逻辑判断", "条件逻辑",
    "传导", "链条", "多步",
)

_SUITABLE_KEYWORDS = (
    "累积", "积累", "压力", "负担", "聚集",
    "反馈循环", "循环", "飞轮", "加速",
    "拉扯", "张力", "对抗", "两方", "矛盾",
    "表面", "隐藏", "脆弱", "裂纹", "稳，只是",
    "状态切换", "转变", "跨越", "门槛",
    "网络效应", "传播", "节点",
    "信息过载", "溢出", "容器",
)

# Visual case mapping keywords → (visual_case_id, route)
_CASE_KEYWORDS: dict[str, tuple[str, str]] = {
    "累积": ("burden-growth", "structured_hybrid"),
    "积累": ("burden-growth", "structured_hybrid"),
    "压力": ("burden-growth", "structured_hybrid"),
    "负担": ("burden-growth", "structured_hybrid"),
    "承诺": ("burden-growth", "structured_hybrid"),
    "资源占用": ("burden-growth", "structured_hybrid"),
    "循环": ("speed-loop", "structured_hybrid"),
    "反馈": ("speed-loop", "structured_hybrid"),
    "飞轮": ("speed-loop", "structured_hybrid"),
    "加速": ("speed-loop", "structured_hybrid"),
    "体验改善": ("speed-loop", "structured_hybrid"),
    "用户增长": ("speed-loop", "structured_hybrid"),
    "拉扯": ("tug-of-war", "approved_still"),
    "张力": ("tug-of-war", "approved_still"),
    "对抗": ("tug-of-war", "approved_still"),
    "两方": ("tug-of-war", "approved_still"),
    "矛盾": ("tug-of-war", "approved_still"),
    "增长与风险": ("tug-of-war", "approved_still"),
    "表面": ("hidden-fragility", "approved_still"),
    "隐藏": ("hidden-fragility", "approved_still"),
    "脆弱": ("hidden-fragility", "approved_still"),
    "裂纹": ("hidden-fragility", "approved_still"),
    "稳，只是": ("hidden-fragility", "approved_still"),
    "网络": ("network-effect", "structured_hybrid"),
    "节点": ("network-effect", "structured_hybrid"),
    "传播": ("network-effect", "structured_hybrid"),
    "传导": ("network-effect", "structured_hybrid"),
    "信息": ("information-overload", "structured_hybrid"),
    "过载": ("information-overload", "structured_hybrid"),
    "溢出": ("information-overload", "structured_hybrid"),
    "卡片": ("information-overload", "structured_hybrid"),
    "切换": ("state-transition", "structured_hybrid"),
    "转变": ("state-transition", "structured_hybrid"),
    "跨越": ("state-transition", "structured_hybrid"),
    "门槛": ("state-transition", "structured_hybrid"),
    "规则改变": ("state-transition", "structured_hybrid"),
    "规则变化": ("state-transition", "structured_hybrid"),
    "路径变化": ("state-transition", "structured_hybrid"),
}


# --- Utility functions ------------------------------------------------------

def _canonical_json(value: Any) -> str:
    """Canonical JSON serialization for hashing."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


# --- Suitability assessment -------------------------------------------------

def assess_suitability(opportunity: dict) -> tuple[str, str, str]:
    """Assess suitability of an Opportunity for the Illustrated Metaphor family.

    Returns (suitability, reason, visual_case_id).
    Pure function; no I/O, no fixture lookup.
    """
    semantics = str(opportunity.get("spoken_semantics", ""))
    purpose = str(opportunity.get("visual_purpose", ""))
    combined = f"{semantics} {purpose}"

    # ABSTAIN: exact numeric evidence, percentages, data comparison
    for keyword in _ABSTAIN_KEYWORDS:
        if keyword in combined:
            return (
                "ABSTAIN",
                (f"精确数值、百分比或数据比较属于装饰性隐喻，会牺牲证据精度。"
                 f"触发关键词: {keyword}"),
                "",
            )

    # BORDERLINE: dense causal chains, conditional logical judgments, core business judgments
    for keyword in _BORDERLINE_KEYWORDS:
        if keyword in combined:
            case_id, _route = _select_case(semantics, purpose)
            return (
                "BORDERLINE",
                (f"隐喻可表达过渡但无法精确承载密集因果链或条件逻辑判断。"
                 f"触发关键词: {keyword}"),
                case_id,
            )

    # SUITABLE: accumulation/pressure, feedback loops, tension, surface-vs-mechanism, state changes
    for keyword in _SUITABLE_KEYWORDS:
        if keyword in combined:
            case_id, _route = _select_case(semantics, purpose)
            return (
                "SUITABLE",
                (f"物理隐喻是 Illustrated Metaphor 的天然强项，可表达积累/压力/循环/张力/表面-机制/状态变化。"
                 f"触发关键词: {keyword}"),
                case_id,
            )

    # Default: BORDERLINE for unrecognized semantics — conservative
    case_id, _route = _select_case(semantics, purpose)
    return (
        "BORDERLINE",
        "无法精确匹配 Illustrated Metaphor 家族能力边界，保守判定为 BORDERLINE。",
        case_id,
    )


def _select_case(semantics: str, purpose: str = "") -> tuple[str, str]:
    """Map text to the best-fit visual case ID and route.

    Prioritises spoken_semantics over visual_purpose.
    Returns (visual_case_id, route).
    Pure function; no fixture lookup.
    """
    # Search semantics first, then purpose as fallback
    for text in (semantics, purpose):
        for keyword, (case_id, route) in _CASE_KEYWORDS.items():
            if keyword in text:
                return case_id, route
    return "burden-growth", "structured_hybrid"  # default


def map_opportunity_to_case(opportunity: dict) -> tuple[str, str]:
    """Map an Opportunity to (visual_case_id, route).

    If suitability is ABSTAIN, returns ("", "none").
    Pure function.
    """
    suitability, _reason, visual_case_id = assess_suitability(opportunity)
    if suitability == "ABSTAIN":
        return "", "none"
    if visual_case_id:
        # Re-select route to ensure consistency
        _, route = _select_case(
            opportunity.get('spoken_semantics', ''),
            opportunity.get('visual_purpose', ''),
        )
        return visual_case_id, route
    # Fallback
    return "burden-growth", "structured_hybrid"


# --- Deterministic ID computation ------------------------------------------

def _opportunity_content_digest(opportunity: dict) -> str:
    """SHA-256 of canonical serialization of Opportunity's material content fields."""
    content = {
        "spoken_semantics": opportunity.get("spoken_semantics", ""),
        "visual_purpose": opportunity.get("visual_purpose", ""),
        "target_duration_ms": opportunity.get("target_duration_ms", 0),
        "canvas": opportunity.get("canvas", {}),
        "language": opportunity.get("language", ""),
    }
    return _sha256_hex(_canonical_json(content))


def compute_proposal_id(
    plugin_id: str,
    plugin_version: str,
    opp_digest: str,
    suitability: str,
    case_id: str,
    route: str,
) -> str:
    """Deterministic proposal_id binding plugin_version + opportunity content + suitability + case mapping."""
    raw = f"{plugin_id}{plugin_version}{opp_digest}{suitability}{case_id}{route}"
    return "prop-im-" + _sha256_hex(raw)[:24]


def _internal_scene_digest(
    visual_case_id: str,
    case_dict: dict,
    duration_ms: int,
) -> str:
    """SHA-256 of the fully-resolved internal scene representation."""
    spec = get_metaphor_spec(visual_case_id)
    scene_repr = {
        "visual_case_id": visual_case_id,
        "case_dict_canonical": _canonical_json({
            "scene_states": case_dict.get("scene_states", []),
            "metaphor_spec": {
                "case_id": spec.case_id,
                "metaphor": spec.metaphor,
                "actor_role": spec.actor_role,
                "objects": list(spec.objects),
                "relation": spec.relation,
                "focal_object": spec.focal_object,
                "state_change": spec.state_change,
                "annotation_position": spec.annotation_position,
                "motion_opportunity": spec.motion_opportunity,
            },
            "candidate_text": case_dict.get("text", ""),
        }),
        "duration_ms": duration_ms,
    }
    return _sha256_hex(_canonical_json(scene_repr))


def _render_settings(canvas_width: int, canvas_height: int) -> str:
    """Canonical serialization of render settings."""
    return _canonical_json({
        "canvas_width": canvas_width,
        "canvas_height": canvas_height,
        "framerate": 24,
        "pix_fmt": "yuv420p",
        "scale_filter": "none" if canvas_width == 1280 else f"scale={canvas_width}:{canvas_height}",
    })


def compute_candidate_id(
    proposal_id: str,
    plugin_version: str,
    internal_scene_digest: str,
    route: str,
    render_settings: str,
) -> str:
    """Deterministic candidate_id binding internal scene + render settings."""
    raw = f"{proposal_id}{plugin_version}{internal_scene_digest}{route}{render_settings}"
    return "cand-im-" + _sha256_hex(raw)[:24]


# --- Candidate text derivation ---------------------------------------------

def _derive_candidate_text(opportunity: dict, visual_case_id: str) -> str:
    """Derive a short Chinese label from the Opportunity's spoken_semantics.

    Deterministic: takes the first clause (before first punctuation)
    or truncates to 20 characters if no clause break is found.
    """
    semantics = str(opportunity.get("spoken_semantics", ""))
    for sep in ("，", "。", "；", ",", ".", ";"):
        if sep in semantics:
            clause = semantics.split(sep)[0]
            if clause.strip():
                return clause.strip()
    return semantics[:20].strip() if semantics else visual_case_id


# --- Duration handling -----------------------------------------------------

def _clamp_duration(target_duration_ms: int) -> int:
    """Clamp to 3–10 seconds (3000–10000 ms)."""
    clamped = max(3000, min(10000, target_duration_ms))
    return clamped


# --- Canvas capability -----------------------------------------------------

def _resolve_canvas(opportunity: dict) -> tuple[int, int, str]:
    """Resolve canvas dimensions.

    Returns (width, height, decision_note).

    Quality-first principle: The SVG viewBox is 1280×720 (hardcoded in art.py).
    We investigate if the vector pipeline can rasterize at the requested canvas.

    The current SVG output is 1280×720. For Contract V1, we test whether sips
    can rasterize the SVG at the requested resolution by modifying the SVG's
    width/height attributes before rasterization. This is done in the runner
    without modifying production source (art.py).

    Decision:
    - If canvas is 1280×720: use natively (no scaling needed).
    - If canvas is 1920×1080: rasterize SVG at 1920×1080 by modifying SVG
      width/height attributes (vector pipeline supports this).
    - For other 16:9 canvases: same approach (modify SVG dimensions).
    - For non-16:9 canvases: declare capability boundary → BLOCKED.
    """
    canvas = opportunity.get("canvas", {})
    width = int(canvas.get("width", 1280))
    height = int(canvas.get("height", 720))

    # Check 16:9 ratio (with tolerance)
    target_ratio = width / height if height > 0 else 0
    is_16_9 = abs(target_ratio - 16.0 / 9.0) < 0.01

    if width == 1280 and height == 720:
        return 1280, 720, "native canvas 1280×720, no scaling needed"
    if is_16_9:
        return width, height, f"vector pipeline rasterize at {width}×{height} (16:9, SVG width/height parameterized)"
    # Non-16:9: capability boundary
    return 1280, 720, f"non-16:9 canvas {width}×{height} not supported; capability boundary declared"


def _is_canvas_supported(opportunity: dict) -> bool:
    """Check if the requested canvas is supported."""
    canvas = opportunity.get("canvas", {})
    width = int(canvas.get("width", 1280))
    height = int(canvas.get("height", 720))
    if width == 1280 and height == 720:
        return True
    target_ratio = width / height if height > 0 else 0
    return abs(target_ratio - 16.0 / 9.0) < 0.01


# --- Suitability response builder ------------------------------------------

def build_suitability_response(request: dict) -> dict:
    """Build a Contract V1 suitability response.

    Pure function (no I/O except it reads nothing external).
    """
    opportunity = request["opportunity"]
    suitability, reason, visual_case_id = assess_suitability(opportunity)

    if suitability == "ABSTAIN":
        case_id, route = "", "none"
    else:
        case_id, route = _select_case(
            opportunity.get('spoken_semantics', ''),
            opportunity.get('visual_purpose', ''),
        )
        if visual_case_id:
            case_id = visual_case_id

    opp_digest = _opportunity_content_digest(opportunity)
    proposal_id = compute_proposal_id(
        PLUGIN_ID, PLUGIN_VERSION, opp_digest, suitability, case_id, route,
    )

    return {
        "contract_version": CONTRACT_VERSION,
        "request_id": request["request_id"],
        "opportunity_id": opportunity["opportunity_id"],
        "plugin_id": PLUGIN_ID,
        "plugin_version": PLUGIN_VERSION,
        "proposal_id": proposal_id,
        "operation_status": "COMPLETED",
        "suitability": suitability,
        "reason": reason,
    }


# --- Generation result builder ---------------------------------------------

def _build_case_dict(visual_case_id: str, candidate_text: str, duration_seconds: int) -> dict:
    """Build a minimal case dict for rendering.

    Constructs in-memory from the hardcoded SPECS — no fixture file I/O.
    """
    get_metaphor_spec(visual_case_id)  # validate case_id is known
    scene_states = [
        {"name": "start"},
        {"name": "change"},
        {"name": "final"},
    ]
    # For 2-state cases, adjust
    if visual_case_id in ("tug-of-war", "speed-loop", "hidden-fragility", "information-overload", "network-effect"):
        scene_states = [{"name": "start"}, {"name": "change"}]
    elif visual_case_id == "state-transition":
        scene_states = [{"name": "reactive"}, {"name": "choice"}, {"name": "active"}]

    return {
        "id": visual_case_id,
        "text": candidate_text,
        "scene_states": scene_states,
        "duration_seconds": duration_seconds,
        "tracks": ["b1_metaphor_system"],
    }


def _translate_qa(qa_result: dict) -> dict:
    """Translate existing QA result to Contract V1 qa field."""
    if qa_result.get("passed"):
        return {
            "status": "PASSED",
            "summary": "all required checks passed",
        }
    failures = qa_result.get("failures", [])
    return {
        "status": "FAILED",
        "summary": "; ".join(failures) if failures else "unknown QA failure",
    }


def _build_artifacts(asset: dict, output_dir: Path, candidate_id: str) -> list[dict]:
    """Build Contract V1 artifact list from rendered asset.

    Ensures every artifact URI points to a real file in output_dir.
    """
    artifacts = []

    # PRIMARY_MEDIA — asset.mp4
    mp4_path = Path(asset["files"][0])
    mp4_rel = mp4_path.relative_to(output_dir)
    artifacts.append({
        "role": "PRIMARY_MEDIA",
        "uri": f"local-runner://{mp4_rel}",
        "media_type": "video/mp4",
        "sha256": hashlib.sha256(mp4_path.read_bytes()).hexdigest(),
    })

    # PREVIEW — contact-sheet.png
    contact_path = Path(asset["files"][1])
    contact_rel = contact_path.relative_to(output_dir)
    artifacts.append({
        "role": "PREVIEW",
        "uri": f"local-runner://{contact_rel}",
        "media_type": "image/png",
    })

    # MANIFEST — manifest.json
    manifest_path = mp4_path.parent / "manifest.json"
    manifest_rel = manifest_path.relative_to(output_dir)
    artifacts.append({
        "role": "MANIFEST",
        "uri": f"local-runner://{manifest_rel}",
        "media_type": "application/json",
    })

    # QA_REPORT — qa-report.json (standalone file, not inside manifest)
    qa_report_path = mp4_path.parent / "qa-report.json"
    qa_report_rel = qa_report_path.relative_to(output_dir)
    artifacts.append({
        "role": "QA_REPORT",
        "uri": f"local-runner://{qa_report_rel}",
        "media_type": "application/json",
    })

    return artifacts


def _scale_svg(svg_path: Path, target_width: int, target_height: int) -> None:
    """Modify SVG width/height attributes for rasterization at target resolution.

    The SVG viewBox is 0 0 1280 720. We keep the viewBox and only change
    width/height so the vector pipeline rasterizes at the target resolution.
    This does NOT modify production source (art.py); it post-processes the
    SVG file that was already generated by the existing pipeline.
    """
    if target_width == 1280 and target_height == 720:
        return
    content = svg_path.read_text(encoding="utf-8")
    content = re.sub(
        r'width="1280" height="720"',
        f'width="{target_width}" height="{target_height}"',
        content,
    )
    svg_path.write_text(content, encoding="utf-8")


def build_generation_result(request: dict, output_dir: Path) -> dict:
    """Build a Contract V1 generation result.

    This function performs actual asset rendering via the existing pipeline.
    Writes artifacts to output_dir and returns the result dict.
    """
    opportunity = request["opportunity"]
    proposal_id = request["proposal_id"]

    # Re-assess suitability for tampering detection
    suitability, _reason, _visual_case_id = assess_suitability(opportunity)
    case_id, route = map_opportunity_to_case(opportunity)

    # Tampering detection: recompute opportunity digest and compare
    opp_digest = _opportunity_content_digest(opportunity)
    recomputed_proposal_id = compute_proposal_id(
        PLUGIN_ID, PLUGIN_VERSION, opp_digest, suitability, case_id, route,
    )
    if recomputed_proposal_id != proposal_id:
        return {
            "contract_version": CONTRACT_VERSION,
            "request_id": request["request_id"],
            "opportunity_id": opportunity["opportunity_id"],
            "proposal_id": proposal_id,
            "plugin_id": PLUGIN_ID,
            "plugin_version": PLUGIN_VERSION,
            "operation_status": "FAILED",
            "problem": {
                "code": "OPPORTUNITY_CONTENT_MISMATCH",
                "message": "opportunity content digest does not match the proposal_id",
                "retryability": False,
            },
        }

    # Canvas capability check
    if not _is_canvas_supported(opportunity):
        canvas = opportunity.get("canvas", {})
        return {
            "contract_version": CONTRACT_VERSION,
            "request_id": request["request_id"],
            "opportunity_id": opportunity["opportunity_id"],
            "proposal_id": proposal_id,
            "plugin_id": PLUGIN_ID,
            "plugin_version": PLUGIN_VERSION,
            "operation_status": "BLOCKED",
            "problem": {
                "code": "UNSUPPORTED_CANVAS",
                "message": f"canvas {canvas.get('width', 0)}×{canvas.get('height', 0)} is not a 16:9 ratio; capability boundary",
                "retryability": False,
            },
        }

    canvas_w, canvas_h, canvas_note = _resolve_canvas(opportunity)

    # Duration
    target_duration_ms = _clamp_duration(int(opportunity.get("target_duration_ms", 5000)))
    duration_seconds = target_duration_ms // 1000

    # Build case dict
    candidate_text = _derive_candidate_text(opportunity, case_id)
    case_dict = _build_case_dict(case_id, candidate_text, duration_seconds)

    # Compute candidate_id
    scene_digest = _internal_scene_digest(case_id, case_dict, target_duration_ms)
    r_settings = _render_settings(canvas_w, canvas_h)
    candidate_id = compute_candidate_id(
        proposal_id, PLUGIN_VERSION, scene_digest, route, r_settings,
    )

    # Render the asset using existing pipeline
    final_state = len(case_dict["scene_states"]) - 1 if route == "approved_still" else 0
    asset = _render_asset(
        output_dir,
        case_dict,
        "b1_metaphor_system",
        route,
        approved_state_index=final_state,
        asset_id=candidate_id,
        manifest_case_id=opportunity.get("opportunity_id", case_id),
        metadata={
            "study": "contract-v1",
            "spoken_semantics": opportunity.get("spoken_semantics", ""),
            "visual_purpose": opportunity.get("visual_purpose", ""),
        },
    )

    # Scale SVG files for requested canvas (post-process, not modifying production source)
    if canvas_w != 1280 or canvas_h != 720:
        frame_dir = output_dir / candidate_id / "b1_metaphor_system" / route / "sequence"
        for svg_file in frame_dir.glob("*.svg"):
            _scale_svg(svg_file, canvas_w, canvas_h)
        # Re-rasterize PNGs at target resolution
        from .render import _run
        for svg_file in sorted(frame_dir.glob("*.svg")):
            png_file = svg_file.with_suffix(".png")
            _run(["sips", "-s", "format", "png", str(svg_file), "--out", str(png_file)])
        # Re-assemble MP4 with metadata stripping for determinism
        mp4_path = frame_dir.parent / "asset.mp4"
        pattern = str(frame_dir / "frame_%03d.png")
        frame_count = len(case_dict["scene_states"]) if route != "approved_still" else 1
        # Use the same assembly parameters but add -map_metadata -1
        if route == "approved_still":
            source = pattern.replace("%03d", "001")
            zoom = f"zoompan=z='min(zoom+0.00035,1.035)':x='iw/2-(iw/zoom/2)+on*0.05':y='ih/2-(ih/zoom/2)':d={duration_seconds * 24}:s={canvas_w}x{canvas_h}:fps=24,fade=t=in:st=0:d=0.35"
            _run(["ffmpeg", "-y", "-loop", "1", "-i", source, "-vf", zoom, "-t", str(duration_seconds), "-r", "24", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-map_metadata", "-1", str(mp4_path)])
        else:
            framerate = frame_count / duration_seconds
            _run(["ffmpeg", "-y", "-framerate", str(framerate), "-i", pattern, "-r", "24", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-map_metadata", "-1", str(mp4_path)])
        # Re-generate contact sheet
        from .render import contact_sheet
        contact_path = frame_dir.parent / "contact-sheet.png"
        contact_sheet(pattern, frame_count, contact_path)
        # Update files list
        asset["files"] = [str(mp4_path), str(contact_path)] + [str(p) for p in sorted(frame_dir.glob("*.png"))]
        asset["sequence_sha256"] = hashlib.sha256(
            b"".join(Path(item).read_bytes() for item in asset["files"][2:])
        ).hexdigest()
        asset["qa"] = asset.get("qa", {})  # Keep existing QA
        # Re-write manifest
        (frame_dir.parent / "manifest.json").write_text(
            json.dumps(asset, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    else:
        # For 1280×720, still strip MP4 metadata for determinism
        from .render import _run
        frame_dir = output_dir / candidate_id / "b1_metaphor_system" / route / "sequence"
        mp4_path = frame_dir.parent / "asset.mp4"
        pattern = str(frame_dir / "frame_%03d.png")
        frame_count = len(case_dict["scene_states"]) if route != "approved_still" else 1
        if route == "approved_still":
            source = pattern.replace("%03d", "001")
            zoom = f"zoompan=z='min(zoom+0.00035,1.035)':x='iw/2-(iw/zoom/2)+on*0.05':y='ih/2-(ih/zoom/2)':d={duration_seconds * 24}:s=1280x720:fps=24,fade=t=in:st=0:d=0.35"
            _run(["ffmpeg", "-y", "-loop", "1", "-i", source, "-vf", zoom, "-t", str(duration_seconds), "-r", "24", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-map_metadata", "-1", str(mp4_path)])
        else:
            framerate = frame_count / duration_seconds
            _run(["ffmpeg", "-y", "-framerate", str(framerate), "-i", pattern, "-r", "24", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-map_metadata", "-1", str(mp4_path)])

    # Write standalone qa-report.json
    qa_translated = _translate_qa(asset.get("qa", {"passed": False, "failures": ["no QA data"]}))
    qa_report_path = output_dir / candidate_id / "b1_metaphor_system" / route / "qa-report.json"
    qa_report_path.parent.mkdir(parents=True, exist_ok=True)
    qa_report_path.write_text(
        json.dumps(qa_translated, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )

    # Build artifacts
    artifacts = _build_artifacts(asset, output_dir, candidate_id)

    # Build candidate
    a_roll_window = opportunity.get("a_roll_window", {"start_ms": 0, "end_ms": target_duration_ms})
    suggested_placement = {
        "start_ms": a_roll_window["start_ms"],
        "end_ms": a_roll_window["end_ms"],
    }

    # Determine candidate status from QA
    candidate_status = "READY" if qa_translated["status"] == "PASSED" else "QA_REJECTED"

    candidate = {
        "candidate_id": candidate_id,
        "asset_family": ASSET_FAMILY,
        "candidate_status": candidate_status,
        "duration_ms": target_duration_ms,
        "suggested_placement": suggested_placement,
        "artifacts": artifacts,
        "qa": qa_translated,
        "provenance": {
            "origin": "plugin-generated",
            "source_ref": "illustrated-metaphor manifest",
        },
        "plugin_metadata": {
            "visual_case_id": case_id,
            "route": route,
            "canvas": {"width": canvas_w, "height": canvas_h},
            "canvas_decision": canvas_note,
            "render_settings": r_settings,
            "internal_scene_digest": scene_digest,
        },
    }

    return {
        "contract_version": CONTRACT_VERSION,
        "request_id": request["request_id"],
        "opportunity_id": opportunity["opportunity_id"],
        "proposal_id": proposal_id,
        "plugin_id": PLUGIN_ID,
        "plugin_version": PLUGIN_VERSION,
        "operation_status": "COMPLETED",
        "candidate": candidate,
    }
