import arcpy

from ..utils import geojson_helper


def aoi_parameter():
    param = arcpy.Parameter(
        displayName="Area Of Interest",
        name="aoi",
        datatype="GPFeatureRecordSetLayer",
        parameterType="Required",
        direction="Input",
    )
    param.filter.list = ["Point"]
    return param


def validate_aoi_parameter(parameter):
    if parameter.value is not None:
        if aoi_has_features(parameter.value) == False:
            parameter.setErrorMessage(
                "AOI must contain features. After adding features, clear AOI parameter and re-select layer."
            )


def aoi_has_features(aoi_selection):
    result = arcpy.GetCount_management(aoi_selection)
    return int(result.getOutput(0)) > 0


def buffer_parameter():
    param = arcpy.Parameter(
        displayName="Buffer (km)",
        name="buffer",
        datatype="GPDouble",
        parameterType="Required",
        direction="Input",
    )
    param.value = 2.5
    param.filter.type = "Range"
    param.filter.list = [1, 5]
    return param


def build_aoi_from_feature_set(feature_set, buffer_km):
    feature_collection = geojson_helper.esri_json_to_geojson(feature_set.JSON)
    return [
        build_aoi_from_geojson_feature(feature, buffer_km)
        for feature in feature_collection["features"]
    ]


def build_aoi_from_feature_class(feature_class, buffer_km):
    feature_collection = geojson_helper.feature_class_to_geojson(feature_class)
    return [
        build_aoi_from_geojson_feature(feature, buffer_km)
        for feature in feature_collection["features"]
    ]


def build_aoi_from_geojson_feature(point_feature, buffer_km):
    return {
        "type": "point",
        "latitude_deg": round(point_feature["geometry"]["coordinates"][1], 5),
        "longitude_deg": round(point_feature["geometry"]["coordinates"][0], 5),
        "radius_km": buffer_km,
    }


def build_aois_from_aoi_parameters(aoi_parameter, buffer_parameter):
    aoi_param_describe = arcpy.Describe(aoi_parameter.value)
    if aoi_param_describe.dataType == "FeatureRecordSetLayer":
        return build_aoi_from_feature_set(aoi_parameter.value, buffer_parameter.value)
    elif (
        aoi_param_describe.dataType == "ShapeFile"
        or aoi_param_describe.dataType == "FeatureClass"
    ):
        return build_aoi_from_feature_class(
            aoi_param_describe.catalogPath, buffer_parameter.value
        )
    elif aoi_param_describe.dataType == "FeatureLayer":
        return build_aoi_from_feature_class(
            aoi_param_describe.featureClass.catalogPath, buffer_parameter.value
        )
    else:
        raise TypeError(
            "AOI must be type FeatureRecordSetLayer, ShapeFile, FeatureClass, or FeatureLayer"
        )
