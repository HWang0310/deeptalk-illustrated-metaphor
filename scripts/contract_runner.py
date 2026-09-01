#!/usr/bin/env python3
"""Contract V1 runner entry point for Illustrated Metaphor.

Flags:
  --version                    Print plugin version, exit 0
  --request <path>             Read request JSON
  --result <path>              Write result JSON (atomic)
  --output-dir <path>          Write artifacts to this directory

The runner routes to suitability or generation based on proposal_id presence.
"""

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from illustrated_metaphor.contract import (
    CONTRACT_VERSION,
    PLUGIN_VERSION,
    build_generation_result,
    build_suitability_response,
)


def _write_atomic(result_path: Path, data: dict) -> None:
    """Write JSON atomically via temp file + os.replace()."""
    temp_path = result_path.with_suffix(".tmp")
    temp_path.write_text(
        json.dumps(data, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )
    os.replace(temp_path, result_path)


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)

    parser = argparse.ArgumentParser(description="Illustrated Metaphor Contract V1 Runner")
    parser.add_argument("--version", action="store_true")
    parser.add_argument("--request", type=Path)
    parser.add_argument("--result", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parsed = parser.parse_args(args)

    # --version: print single-line version, exit 0
    if parsed.version:
        print(PLUGIN_VERSION)
        return 0

    # Request/result/output-dir mode
    if not parsed.request or not parsed.result or not parsed.output_dir:
        print("usage: contract_runner.py --request <path> --result <path> --output-dir <path>", file=sys.stderr)
        return 1

    # Case B: malformed request — fail closed (non-zero exit, no result file)
    try:
        request = json.loads(parsed.request.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        print("error: cannot parse request JSON", file=sys.stderr)
        return 1

    # Validate contract version
    if request.get("contract_version") != CONTRACT_VERSION:
        print(f"error: contract_version must be {CONTRACT_VERSION}", file=sys.stderr)
        return 1

    # Validate required fields
    if "request_id" not in request or "opportunity" not in request:
        print("error: missing request_id or opportunity", file=sys.stderr)
        return 1

    # Route: generation if proposal_id present, suitability otherwise
    is_generation = "proposal_id" in request

    try:
        if is_generation:
            # Validate proposal_id
            if not isinstance(request.get("proposal_id"), str) or not request["proposal_id"].strip():
                print("error: invalid proposal_id", file=sys.stderr)
                return 1
            parsed.output_dir.mkdir(parents=True, exist_ok=True)
            result = build_generation_result(request, parsed.output_dir)
        else:
            result = build_suitability_response(request)
    except Exception as exc:  # noqa: BLE001
        # Case B: runtime failure — fail closed
        print(f"error: runner failure: {exc}", file=sys.stderr)
        return 1

    # Atomic write
    _write_atomic(parsed.result, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
