"""!
********************************************************************************
@file   app_data.py
@brief  Data module (constants and functions related to path and ini file)
********************************************************************************
"""

import sys
import os
import enum
import logging

from Source.version import __title__

log = logging.getLogger(__title__)


def resource_path(s_relative_path: str) -> str:
    """!
    @brief Returns the absolute path to a resource given by a relative path depending on the environment (EXE or Python)
    @param s_relative_path : the relative path to a file or directory
    @return absolute path to the resource
    """
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        s_base_path = sys._MEIPASS
    else:
        s_base_path = os.path.abspath("../")
    s_resource_path = os.path.join(s_base_path, s_relative_path)
    log.debug("Resource Path (relative %s): %s", s_relative_path, s_resource_path)
    return s_resource_path


# Files and Paths
ICON_APP_PATH = "Resources/app.ico"
ICON_APP_FAVICON_PATH = "Resources/favicon.ico"
ICON_APP = resource_path(ICON_APP_PATH)


class ETheme(str, enum.Enum):
    """!
    @brief Available application themes
    """
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"
