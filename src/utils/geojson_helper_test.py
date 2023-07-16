import unittest
import arcpy
import os

from . import geojson_helper


class GeojsonHelperTestCase(unittest.TestCase):
    MOCK_POINT_SHP = "MOCK_POINT.shp"

    def setUp(self):
        # set arcpy workspace to mock data directory
        arcpy.env.workspace = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "mock_data",
            )
        )

    def test_feature_class_to_geojson(self):
        geojson = geojson_helper.feature_class_to_geojson(self.MOCK_POINT_SHP)

        self.assertEqual(
            geojson,
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "id": 0,
                        "geometry": {
                            "type": "Point",
                            "coordinates": [
                                -76.49728323840485,
                                42.440759898132285,
                            ],
                        },
                        "properties": {"FID": 0, "name": "test"},
                    }
                ],
            },
        )
