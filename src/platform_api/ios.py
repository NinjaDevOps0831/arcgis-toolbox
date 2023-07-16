import requests

from .. import config
from . import auth_token


def post_order(order_object):
    headers = {
        "Authorization": "Bearer {}".format(auth_token.token),
        "Content-Type": "application/json",
    }

    order_url = "{}/api/ios/order".format(config.baseUrl)

    return requests.post(
        url=order_url,
        headers=headers,
        json=order_object,
    )


def build_collection_parameters(imaging_mode, resolution_meters, vendor_preferences):
    return [
        {
            "type": "sar",
            "imagingMode": imaging_mode,
            "resolutionMeters": resolution_meters,
            "vendorPreferences": vendor_preferences,
        }
    ]


def build_tasking_order(email, aois, schedule, collection_params):
    return build_order(
        {
            "contactEmail": email,
            "requireApproval": True,
            "type": "tasking-parameters",
            "aois": aois,
            "schedule": schedule,
            "collectionParameters": collection_params,
        }
    )


def build_analytics_order(email, aois, schedule, workflow_request, cd_params=None):
    req = {
        "contactEmail": email,
        "requireApproval": True,
        "type": "workflow",
        "aois": aois,
        "schedule": schedule,
        "workflowRequest": workflow_request,
    }

    if cd_params is not None:
        req["changeDetAnalyticParams"] = cd_params

    return build_order(req)


def build_order(request):
    return {"customerNotes": "#ESRI-TOOLBOX", "request": request}


def cancel_order(id: str):
    headers = {"Authorization": "Bearer {}".format(auth_token.token)}

    cancel_url = "{}/api/ios/order/{}/cancel".format(config.baseUrl, id)

    return requests.post(
        url=cancel_url,
        headers=headers,
    )


def handle_order_success(resp: requests.Response, messages):
    resp_json = resp.json()
    if resp_json["statusHistory"][-1]["state"] == "in-progress":
        handle_invoice_customer(resp_json["id"], messages)
    else:
        handle_stripe_customer(resp_json["id"], messages)


def handle_order_failure(resp: requests.Response, messages):
    messages.addErrorMessage({"status_code": resp.status_code, "reason": resp.reason})


def handle_invoice_customer(order_id: str, messages):
    messages.addMessage("Order Submitted!")
    messages.addMessage("Order Number: {}".format(order_id))
    messages.addMessage(
        "You will receive an email confirmation with full order details shortly."
    )


def handle_stripe_customer(order_id: str, messages):
    cancel_order(order_id)
    messages.addErrorMessage(
        "Must be an invoice customer to submit orders. Please contact support@ursaspace.com."
    )


def handle_l1_user(messages):
    messages.addErrorMessage(
        "Must be an L2 User to submit orders. Please contact support@ursaspace.com."
    )
