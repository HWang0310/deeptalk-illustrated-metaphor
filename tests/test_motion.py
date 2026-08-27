import tempfile
import unittest
from pathlib import Path

from illustrated_metaphor.motion import build_route


CASE = {
    "id": "burden-growth",
    "duration_seconds": 5,
    "scene_states": [{"name": "start"}, {"name": "strain"}, {"name": "overwhelm"}],
}


class MotionTests(unittest.TestCase):
    def test_all_routes_plan_ordered_states_and_duration(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            for route in ("approved_still", "structured_hybrid", "independent_keyframes"):
                manifest = build_route(route, CASE, Path(temporary_directory))
                self.assertEqual(route, manifest["route"])
                self.assertEqual(5, manifest["duration_seconds"])
                self.assertEqual(["start", "strain", "overwhelm"], manifest["state_names"])
                self.assertGreaterEqual(len(manifest["frame_plan"]), 2)

