import arcpy


def password_parameter():
    return arcpy.Parameter(
        displayName="Password",
        name="password",
        datatype="GPStringHidden",
        direction="input",
        parameterType="required",
    )
