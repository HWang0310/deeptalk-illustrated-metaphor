import unittest

from illustrated_metaphor.scene import validate_scene


class SceneTests(unittest.TestCase):
    def test_rejects_invalid_duration_and_unnamed_state(self):
        errors = validate_scene({"duration_seconds": 2, "scene_states": [{"name": ""}]})

        self.assertIn("duration_seconds must be between 3 and 10", errors)
        self.assertIn("scene_states[0].name is required", errors)

