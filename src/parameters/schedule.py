import datetime

import arcpy


def start_date_parameter():
    param = arcpy.Parameter(
        displayName="Start Date",
        name="startDate",
        datatype="GPDate",
        parameterType="Required",
        direction="Input",
    )
    # give user 1 hour buffer by default to complete order within required 48hr window
    param.value = get_minimum_start_date() + datetime.timedelta(hours=1)
    return param


def validate_start_date_parameter(parameter):
    if parameter.value:
        min_date = get_minimum_start_date()
        if parameter.value < min_date:
            parameter.setErrorMessage("Minimum Start Date must be {}".format(min_date))


def end_date_parameter():
    param = arcpy.Parameter(
        displayName="End Date",
        name="endDate",
        datatype="GPDate",
        parameterType="Required",
        direction="Input",
    )
    param.value = (get_minimum_start_date() + datetime.timedelta(hours=24)).replace(
        hour=23, minute=59
    )
    return param


def validate_end_date_parameter(start_parameter, end_parameter):
    if start_parameter.value and end_parameter.value:
        if start_parameter.value == end_parameter.value:
            end_parameter.setWarningMessage(
                "Increase range to improve probability of successful order."
            )
        if start_parameter.value > end_parameter.value:
            end_parameter.setErrorMessage("End Date cannot precede Start Date.")


def get_minimum_start_date():
    return datetime.datetime.now() + datetime.timedelta(hours=48)


def build_schedule(start_date: datetime.date, end_date: datetime.date):
    return [
        {
            "type": "range",
            "range": {"min": start_date.isoformat(), "max": end_date.isoformat()},
        }
    ]
