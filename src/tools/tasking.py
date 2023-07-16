import importlib
from typing import List

import arcpy

from ..platform_api import auth_token, ios
from ..utils import jwt_helper
from ..parameters import aoi, imaging_mode, schedule, vendors


class Tasking(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tasking"
        self.description = "New Image Tasking"
        self.canRunInBackground = False

        # trigger reload for hmr development
        importlib.reload(ios)
        importlib.reload(jwt_helper)
        importlib.reload(aoi)
        importlib.reload(imaging_mode)
        importlib.reload(schedule)
        importlib.reload(vendors)

    def getParameterInfo(self):
        """Define parameter definitions"""
        return [
            aoi.aoi_parameter(),
            aoi.buffer_parameter(),
            schedule.start_date_parameter(),
            schedule.end_date_parameter(),
            imaging_mode.imaging_mode_parameter(),
            vendors.preferred_vendors_parameter(),
        ]

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        aoi.validate_aoi_parameter(parameters[0])
        schedule.validate_start_date_parameter(parameters[2])
        schedule.validate_end_date_parameter(parameters[2], parameters[3])

    def execute(self, parameters, messages):
        """The source code of the tool."""
        if jwt_helper.has_role(auth_token.token, "IOS.Order.Create"):
            messages.addMessage("Building Order...")
            email = jwt_helper.email_from_jwt(auth_token.token)
            order = self.tasking_order_from_parameters(email, parameters)

            messages.addMessage("Submitting Order...")
            resp = ios.post_order(order)

            if resp.status_code == 201:
                ios.handle_order_success(resp, messages)
            else:
                ios.handle_order_failure(resp, messages)
        else:
            ios.handle_l1_user(messages)

    def tasking_order_from_parameters(
        self, email: str, parameters: List[arcpy.Parameter]
    ):
        aoi_obj = aoi.build_aois_from_aoi_parameters(
            aoi_parameter=parameters[0], buffer_parameter=parameters[1]
        )

        schedule_obj = schedule.build_schedule(
            start_date=parameters[2].value, end_date=parameters[3].value
        )

        mode = imaging_mode.build_imaging_mode(mode=parameters[4].value)

        resolution = imaging_mode.build_resolution_meters(mode=parameters[4].value)

        vendors_obj = vendors.build_vendor_preferences(vendors=parameters[5].values)

        collection_parameters = ios.build_collection_parameters(
            imaging_mode=mode,
            resolution_meters=resolution,
            vendor_preferences=vendors_obj,
        )

        ios_order = ios.build_tasking_order(
            email=email,
            aois=aoi_obj,
            schedule=schedule_obj,
            collection_params=collection_parameters,
        )

        return ios_order
