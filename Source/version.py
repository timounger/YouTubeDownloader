# This Python file uses the following encoding: utf-8
"""
*****************************************************************************
 @file    version.py
 @brief   YouTubeDownloader - Version and general information
*****************************************************************************
"""

# Version
VERSION_MAJOR = 1 # major changes/breaks at API (e.g incompatibility)
VERSION_MINOR = 0 # minor changes/does not break the API (e.g new feature)
VERSION_PATCH = 2 # Bug fixes
VERSION_BUILD = 2 # build number (if available)


__title__ = "YouTube Downloader"
__description__ = "YouTube content downloader"
__copyright__ = "Copyright © 2021-2023 Timo Unger"
__license__ = "GNU General Public License"
__home__ = "https://timounger.github.io/YouTubeDownloader"

if VERSION_BUILD == 0:
    PRERELEASE_BUILD = False
    __version__ = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"
else:
    PRERELEASE_BUILD = True # Mark the FW as a pre-release build and protect it from unauthorized use.
    __version__ = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}.{VERSION_BUILD}"
