import unittest

from . import imaging_mode


class ImagingModeTestCase(unittest.TestCase):
    def test_build_imaging_mode(self):
        MOCK_MODE = "SPOTLIGHT"
        self.assertEqual(
            imaging_mode.build_imaging_mode(MOCK_MODE),
            {"constraint": MOCK_MODE, "level": "required"},
        )

    def test_build_resolution_meters(self):
        # if mode is SPOTLIGHT
        self.assertEqual(
            imaging_mode.build_resolution_meters("SPOTLIGHT"),
            {"constraint": {"min": 0.5, "max": 1.5}, "level": "required"},
        )

        # if mode is STRIPMAP
        self.assertEqual(
            imaging_mode.build_resolution_meters("STRIPMAP"),
            {"constraint": {"min": 0.5, "max": 3.5}, "level": "required"},
        )
