import unittest
import os

import arcpy

from . import aoi


class AoiTestCase(unittest.TestCase):
    MOCK_FEATURE_CLASS = "MOCK_POINT.shp"
    MOCK_BUFFER = 2

    def setUp(self):
        # set arcpy workspace to mock data directory
        arcpy.env.workspace = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "mock_data",
            )
        )

    def test_build_aoi_from_feature_set(self):
        # create feature set from mock feature class
        MOCK_FEATURE_SET = arcpy.FeatureSet(self.MOCK_FEATURE_CLASS)

        aoi_obj = aoi.build_aoi_from_feature_set(MOCK_FEATURE_SET, self.MOCK_BUFFER)

        self.assertEqual(
            aoi_obj,
            [
                {
                    "type": "point",
                    "latitude_deg": 42.44076,
                    "longitude_deg": -76.49728,
                    "radius_km": self.MOCK_BUFFER,
                }
            ],
        )

    def test_build_aoi_from_feature_class(self):
        aoi_obj = aoi.build_aoi_from_feature_class(
            self.MOCK_FEATURE_CLASS, self.MOCK_BUFFER
        )

        self.assertEqual(
            aoi_obj,
            [
                {
                    "type": "point",
                    "latitude_deg": 42.44076,
                    "longitude_deg": -76.49728,
                    "radius_km": self.MOCK_BUFFER,
                }
            ],
        )

    def test_build_aoi_from_geojson_feature(self):
        MOCK_GEOJSON_FEATURE = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [0, 1]},
            "properties": {},
        }

        aoi_obj = aoi.build_aoi_from_geojson_feature(
            MOCK_GEOJSON_FEATURE, self.MOCK_BUFFER
        )

        self.assertEqual(
            aoi_obj,
            {
                "type": "point",
                "latitude_deg": 1,
                "longitude_deg": 0,
                "radius_km": self.MOCK_BUFFER,
            },
        )
