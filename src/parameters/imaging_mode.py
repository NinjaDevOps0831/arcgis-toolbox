import arcpy


def imaging_mode_parameter():
    param = arcpy.Parameter(
        displayName="Imaging Mode",
        name="imagingMode",
        datatype="GPString",
        parameterType="Required",
        direction="Input",
    )
    param.value = "SPOTLIGHT"
    param.filter.type = "ValueList"
    param.filter.list = ["SPOTLIGHT", "STRIPMAP"]
    return param


def build_imaging_mode(mode: str):
    return {"constraint": mode, "level": "required"}


def resolution_from_mode(mode: str):
    if mode == "SPOTLIGHT":
        return {"min": 0.5, "max": 1.5}
    elif mode == "STRIPMAP":
        return {"min": 0.5, "max": 3.5}
    else:
        return None


def build_resolution_meters(mode: str):
    resolution_obj = resolution_from_mode(mode)
    if resolution_obj != None:
        return {"constraint": resolution_obj, "level": "required"}
    else:
        return None
