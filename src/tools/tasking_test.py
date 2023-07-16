import datetime
import os
import unittest

import arcpy

from . import tasking


class TaskingTestCase(unittest.TestCase):
    tool = tasking.Tasking()
    parameters = []

    MOCK_POINT = "MOCK_POINT.shp"
    MOCK_EMAIL = "brendan.cullen@ursaspace.com"
    MOCK_BUFFER = 3
    MOCK_START = datetime.datetime(2023, 1, 1)
    MOCK_END = datetime.datetime(2023, 1, 2)
    MOCK_MODE = "SPOTLIGHT"
    MOCK_VENDORS = ["ICEYE", "CAPELLA"]

    def setUp(self):
        # set arcpy workspace to mock data directory
        arcpy.env.workspace = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "mock_data",
            )
        )

        # build parameters + set values
        self.parameters = self.tool.getParameterInfo()

        # arcpy param wont load data when setting value
        # so need to assign FeatureSet with schema and then load...
        self.parameters[0].value = arcpy.FeatureSet(
            os.path.join(arcpy.env.workspace, self.MOCK_POINT)
        )
        self.parameters[0].value.load(
            os.path.join(arcpy.env.workspace, self.MOCK_POINT)
        )

        self.parameters[1].value = self.MOCK_BUFFER
        self.parameters[2].value = self.MOCK_START
        self.parameters[3].value = self.MOCK_END
        self.parameters[4].value = self.MOCK_MODE
        self.parameters[5].value = self.MOCK_VENDORS

    def test_tasking_order_from_parameters(self):
        tasking_order = self.tool.tasking_order_from_parameters(
            self.MOCK_EMAIL, self.parameters
        )

        self.assertEqual(
            tasking_order,
            {
                "customerNotes": "#ESRI-TOOLBOX",
                "request": {
                    "contactEmail": self.MOCK_EMAIL,
                    "requireApproval": True,
                    "type": "tasking-parameters",
                    "aois": [
                        {
                            "type": "point",
                            "latitude_deg": 42.44076,
                            "longitude_deg": -76.49728,
                            "radius_km": self.MOCK_BUFFER,
                        }
                    ],
                    "schedule": [
                        {
                            "type": "range",
                            "range": {
                                "min": self.MOCK_START.isoformat(),
                                "max": self.MOCK_END.isoformat(),
                            },
                        }
                    ],
                    "collectionParameters": [
                        {
                            "type": "sar",
                            "imagingMode": {
                                "constraint": self.MOCK_MODE,
                                "level": "required",
                            },
                            "resolutionMeters": {
                                "constraint": {"min": 0.5, "max": 1.5},
                                "level": "required",
                            },
                            "vendorPreferences": {
                                "CAPELLA": "preferred",
                                "ICEYE": "preferred",
                            },
                        }
                    ],
                },
            },
        )
