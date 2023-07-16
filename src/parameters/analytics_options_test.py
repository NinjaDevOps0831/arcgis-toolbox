import unittest

from . import analytic_options


class AnalyticsTestCase(unittest.TestCase):
    def test_build_workflow_request(self):
        MOCK_ANALYTICS = [
            "Small Vessel Detection",
            "Large Vessel Detection",
            "Object Detection (SPEX)",
        ]

        self.assertEqual(
            analytic_options.build_workflow_request(MOCK_ANALYTICS),
            {
                "type": "analytic",
                "analytics": ["SmallVesselDetection", "LargeVesselDetection", "SPEX"],
            },
        )

    def test_build_cd_analytic_params(self):
        MOCK_PARAMS = [
            "Basic Change Detection",
            "Object Level Change Detection",
            "Port Traffic",
        ]

        self.assertEqual(
            analytic_options.build_cd_analytic_params(MOCK_PARAMS),
            {
                "changeDetectionType": [
                    "CHANGE_DETECTION",
                    "OBJECT_LEVEL",
                    "PORT_TRAFFIC",
                ],
                "maxImageWindowHrs": 24,
            },
        )

        self.assertEqual(
            analytic_options.build_cd_analytic_params(None),
            {
                "changeDetectionType": [],
                "maxImageWindowHrs": 24,
            },
        )

    def test_check_to_enable_cd_param(self):
        analytic_param = analytic_options.analytics_parameter()
        cd_param = analytic_options.change_detection_parameter()

        analytic_param.value = ["Change Detection"]
        analytic_options.check_to_enable_cd_param(analytic_param, cd_param)
        self.assertEqual(cd_param.enabled, True)

        analytic_param.value = []
        analytic_options.check_to_enable_cd_param(analytic_param, cd_param)
        self.assertEqual(cd_param.enabled, False)
