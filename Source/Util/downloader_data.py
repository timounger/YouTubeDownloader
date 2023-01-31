# This Python file uses the following encoding: utf-8
"""
*****************************************************************************
 @file    downloader_data.py
 @brief   YouTubeDownloader - Data module
*****************************************************************************
"""

import sys
import os

B_DEBUG = True

S_YOUTUBE_DOWNLOADER_APPLICATION_NAME = "YouTubeDownloader"
S_YOUTUBE_DOWNLOADER_DESCRIPTION = "YouTube content downloader"

# Version
I_VERSION_MAJOR = 1 # major changes/breaks at API (e.g incompatibility)
I_VERSION_MINOR = 0 # minor changes/does not break the API (e.g new feature)
I_VERSION_PATCH = 0 # Bug fixes
I_VERSION_BUILD = 0 # build number (if available)
S_VERSION = f"{I_VERSION_MAJOR}.{I_VERSION_MINOR}.{I_VERSION_PATCH}"
S_COPYRIGHT = "Copyright © 2021-2023 Timo Unger"
S_LICENSE = "GNU General Public License"
S_HOME = "https://timounger.github.io/YouTubeDownloader"

S_APP_ID = S_YOUTUBE_DOWNLOADER_APPLICATION_NAME + '.' + S_VERSION

def resource_path(s_relative_path: str) -> str:
    """!
    @brief Returns the absolute path to a resource given by a relative path depending on the environment (EXE or Python)
    @param s_relative_path : the relative path to a file or directory
    @return absolute path to the resource
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        s_base_path = sys._MEIPASS # pylint: disable=no-member,protected-access
    except Exception:
        s_base_path = os.path.abspath("../")
    s_resource_path = os.path.join(s_base_path, s_relative_path)
    return s_resource_path

# Files and Paths
S_ICON_RESOURCE_PATH = 'Resources/app.ico'
S_ICON_REL_PATH = resource_path(S_ICON_RESOURCE_PATH)
