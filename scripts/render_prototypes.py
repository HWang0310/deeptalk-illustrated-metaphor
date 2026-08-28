#!/usr/bin/env python3
"""Render local V0 evidence."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from illustrated_metaphor.cli import render_prototypes
from illustrated_metaphor.cli import render_v01_comparison
from illustrated_metaphor.cli import render_v02_comparison


parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path, default=Path("output/v0"))
parser.add_argument("--case-limit", type=int, default=None)
parser.add_argument("--v01-comparison", action="store_true")
parser.add_argument("--v02-comparison", action="store_true")
arguments = parser.parse_args()
result = render_v02_comparison(arguments.output) if arguments.v02_comparison else render_v01_comparison(arguments.output) if arguments.v01_comparison else render_prototypes(arguments.output, arguments.case_limit)
print(f"Rendered {len(result['assets'])} assets to {arguments.output}")
