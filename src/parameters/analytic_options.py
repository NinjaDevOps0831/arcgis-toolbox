from typing import List
import arcpy

# frontend label to backend enum mapping
analytic_map: dict[str, str] = {
    "Small Vessel Detection": "SmallVesselDetection",
    "Large Vessel Detection": "LargeVesselDetection",
    "Aircraft Detection": "AircraftDetection",
    "Ground Vehicle Detection": "GroundVehicleDetection",
    "Car Counting": "CarCounting",
    "Change Detection": "ChangeDetection",
    "Subsidence Monitoring": "SubsidenceMonitoring",
    "Object Detection (SPEX)": "SPEX",
}

# frontend label to backend enum mapping
cd_map: dict[str, str] = {
    "Basic Change Detection": "CHANGE_DETECTION",
    "Object Level Change Detection": "OBJECT_LEVEL",
    "Port Traffic": "PORT_TRAFFIC",
    "Parking Lot": "PARKING_LOT",
    "Construction": "CONSTRUCTION",
    "Hurricane Damage": "HURRICANE_DAMAGE",
    "Large Earth": "LARGE_EARTH",
}


def analytics_parameter() -> arcpy.Parameter:
    param = arcpy.Parameter(
        displayName="Analytic Options",
        name="analyticOptions",
        datatype="GPString",
        parameterType="Required",
        direction="Input",
        multiValue=True,
    )

    param.filter.type = "ValueList"
    param.filter.list = [key for key in analytic_map]
    return param


def change_detection_parameter() -> arcpy.Parameter:
    param = arcpy.Parameter(
        displayName="Change Detection Options",
        name="cdOptions",
        datatype="GPString",
        parameterType="Optional",
        direction="Input",
        multiValue=True,
    )

    param.filter.type = "ValueList"
    param.filter.list = [key for key in cd_map]
    return param


def build_workflow_request(labels: List[str]):
    return {
        "type": "analytic",
        "analytics": [analytic_map[label] for label in labels],
    }


def build_cd_analytic_params(labels: List[str]):
    cd_types = [cd_map[label] for label in labels] if labels else []
    return {
        "changeDetectionType": cd_types,
        "maxImageWindowHrs": 24,
    }


def check_to_enable_cd_param(
    analytic_opt_param: arcpy.Parameter, cd_param: arcpy.Parameter
):
    cd_param.enabled = (
        "Change Detection" in analytic_opt_param.values
        if analytic_opt_param.values is not None
        else False
    )
