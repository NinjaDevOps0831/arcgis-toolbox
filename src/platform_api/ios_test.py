import unittest

import datetime

from . import ios


class IosTestCase(unittest.TestCase):
    MOCK_EMAIL = "test@gmail.com"
    MOCK_AOIS = [
        {
            "type": "point",
            "latitude_deg": 42.44076,
            "longitude_deg": -76.49728,
            "radius_km": 3,
        }
    ]
    MOCK_SCHEDULE = [
        {
            "type": "range",
            "range": {
                "min": datetime.datetime(2023, 1, 1).isoformat(),
                "max": datetime.datetime(2023, 1, 2).isoformat(),
            },
        }
    ]

    def test_build_collection_parameters(self):
        MOCK_IMAGING_MODE = {"constraint": "SPOTLIGHT", "level": "required"}
        MOCK_RESOLUTION = {"constraint": {"min": 0.5, "max": 1.5}, "level": "required"}
        MOCK_VENDORS = {"CAPELLA": "preferred", "ICEYE": "preferred"}

        self.assertEqual(
            ios.build_collection_parameters(
                imaging_mode=MOCK_IMAGING_MODE,
                resolution_meters=MOCK_RESOLUTION,
                vendor_preferences=MOCK_VENDORS,
            ),
            [
                {
                    "type": "sar",
                    "imagingMode": MOCK_IMAGING_MODE,
                    "resolutionMeters": MOCK_RESOLUTION,
                    "vendorPreferences": MOCK_VENDORS,
                }
            ],
        )

    def test_build_tasking_order(self):
        MOCK_COLLECTION_PARAMS = [
            {
                "type": "sar",
                "imagingMode": {"constraint": "SPOTLIGHT", "level": "required"},
                "resolutionMeters": {
                    "constraint": {"min": 0.5, "max": 1.5},
                    "level": "required",
                },
                "vendorPreferences": {"CAPELLA": "preferred", "ICEYE": "preferred"},
            }
        ]

        self.assertEqual(
            ios.build_tasking_order(
                email=self.MOCK_EMAIL,
                aois=self.MOCK_AOIS,
                schedule=self.MOCK_SCHEDULE,
                collection_params=MOCK_COLLECTION_PARAMS,
            ),
            {
                "customerNotes": "#ESRI-TOOLBOX",
                "request": {
                    "contactEmail": self.MOCK_EMAIL,
                    "requireApproval": True,
                    "type": "tasking-parameters",
                    "aois": self.MOCK_AOIS,
                    "schedule": self.MOCK_SCHEDULE,
                    "collectionParameters": MOCK_COLLECTION_PARAMS,
                },
            },
        )

    def test_build_analytics_order(self):
        MOCK_WORKFLOW_REQUEST = {
            "type": "analytic",
            "analytics": [
                "ChangeDetection",
                "SmallVesselDetection",
                "LargeVesselDetection",
            ],
        }
        MOCK_CD_PARAMS = {
            "changeDetectionType": [
                "CHANGE_DETECTION",
                "OBJECT_LEVEL",
                "PORT_TRAFFIC",
            ],
            "maxImageWindowHrs": 24,
        }

        self.assertEqual(
            ios.build_analytics_order(
                email=self.MOCK_EMAIL,
                aois=self.MOCK_AOIS,
                schedule=self.MOCK_SCHEDULE,
                workflow_request=MOCK_WORKFLOW_REQUEST,
                cd_params=MOCK_CD_PARAMS,
            ),
            {
                "customerNotes": "#ESRI-TOOLBOX",
                "request": {
                    "contactEmail": self.MOCK_EMAIL,
                    "requireApproval": True,
                    "type": "workflow",
                    "aois": self.MOCK_AOIS,
                    "schedule": self.MOCK_SCHEDULE,
                    "workflowRequest": MOCK_WORKFLOW_REQUEST,
                    "changeDetAnalyticParams": MOCK_CD_PARAMS,
                },
            },
        )
