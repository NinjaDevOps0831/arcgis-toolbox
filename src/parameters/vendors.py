from typing import List
import arcpy


def preferred_vendors_parameter():
    param = arcpy.Parameter(
        displayName="Preferred Vendors",
        name="preferredVendors",
        datatype="GPString",
        parameterType="Optional",
        direction="Input",
        multiValue=True,
    )
    param.filter.type = "ValueList"
    param.filter.list = ["CAPELLA", "ICEYE"]
    return param


def build_vendor_preferences(vendors: List[str]):
    obj = {}

    if vendors is not None:
        for vendor in vendors:
            obj[vendor] = "preferred"

    return obj
