"""!
********************************************************************************
@file   version.py
@brief  Version and general information
********************************************************************************
"""

# Version
VERSION_MAJOR = 1  # major changes/breaks at API (e.g incompatibility)
VERSION_MINOR = 1  # minor changes/does not break the API (e.g new feature)
VERSION_PATCH = 3  # Bug fixes
VERSION_BUILD = 0  # build number (if available)


__title__ = "YouTubeDownloader"
__description__ = "YouTube content downloader"
__author__ = "Timo Unger"
__owner__ = "timounger"
__repo__ = "YouTubeDownloader"
__copyright__ = f"Copyright © 2021-2025 {__author__}"
__license__ = "GNU General Public License"
__home__ = f"https://{__owner__}.github.io/{__repo__}"


if VERSION_BUILD == 0:
    PRERELEASE_BUILD = False
    __version__ = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"
else:
    PRERELEASE_BUILD = True
    __version__ = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}.{VERSION_BUILD}"
