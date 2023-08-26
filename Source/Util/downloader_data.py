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
S_ICON_RESOURCE_PATH = 'Resources/YouTubeDownloader.ico'
S_ICON_32_RESOURCE_PATH = 'Resources/YouTubeDownloader_32.ico'
S_ICON_REL_PATH = resource_path(S_ICON_RESOURCE_PATH)
