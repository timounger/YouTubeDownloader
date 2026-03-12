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


def resource_path(relative_path: str) -> str:
    """!
    @brief Get the absolute path to a resource given by a relative path depending on the environment (EXE or Python).
    @param relative_path : the relative path to a file or directory.
    @return absolute path to the resource.
    """
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("../"))
    full_path = os.path.join(base_path, relative_path)
    log.debug("Resource Path (relative %s): %s", relative_path, full_path)
    return full_path


# Files and Paths
DOWNLOAD_FOLDER = "Download"
ICON_APP_PATH = "Resources/app.ico"
ICON_APP_FAVICON_PATH = "Resources/favicon.ico"
ICON_APP = resource_path(ICON_APP_PATH)


class ETheme(str, enum.Enum):
    """!
    @brief Available application themes.
    """
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"
