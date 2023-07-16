import importlib

from ..platform_api import auth_token, pas
from ..parameters import username, password


class Login(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Login"
        self.canRunInBackground = False

        # trigger reload for hmr development
        importlib.reload(pas)
        importlib.reload(username)
        importlib.reload(password)

    def getParameterInfo(self):
        """Define parameter definitions"""
        return [username.username_parameter(), password.password_parameter()]

    def execute(self, parameters, messages):
        """The source code of the tool."""
        messages.addMessage("Logging in...")

        resp = pas.login(
            username=parameters[0].valueAsText, password=parameters[1].valueAsText
        )

        if resp.ok:
            auth_token.token = resp.json()["access_token"]
            messages.addMessage("Logged In!")
        else:
            messages.addErrorMessage(
                {"status_code": resp.status_code, "reason": resp.reason}
            )
