import arcpy


def username_parameter():
    return arcpy.Parameter(
        displayName="Username",
        name="username",
        datatype="GPString",
        direction="input",
        parameterType="required",
    )
