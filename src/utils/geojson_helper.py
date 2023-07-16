import arcpy
import json


def esri_json_to_geojson(esri_json):
    fs = arcpy.FeatureSet(json.loads(esri_json))
    return feature_class_to_geojson(fs)


def feature_class_to_geojson(feature_class):
    geojson_path = arcpy.FeaturesToJSON_conversion(
        in_features=feature_class,
        out_json_file="temp_features",
        geoJSON="GEOJSON",
        outputToWGS84="WGS84",
    )

    with open(str(geojson_path)) as file:
        # load geojson from file into memeory
        geojson = json.load(file)

    # delete temp geojson file
    arcpy.Delete_management(geojson_path)

    return geojson
