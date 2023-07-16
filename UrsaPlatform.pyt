import importlib

import src.tools.login as LoginModule
from src.tools.login import Login

import src.tools.tasking as TaskingModule
from src.tools.tasking import Tasking

import src.tools.analytics as AnalyticsModule
from src.tools.analytics import Analytics


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Ursa Platform Toolbox"
        self.alias = "UrsaPlatformToolbox"

        # trigger reload for hmr development
        importlib.reload(LoginModule)
        importlib.reload(TaskingModule)
        importlib.reload(AnalyticsModule)

        # List of tool classes associated with this toolbox
        self.tools = [Login, Tasking, Analytics]
