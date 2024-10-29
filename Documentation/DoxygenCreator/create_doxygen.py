"""!
********************************************************************************
@file   create_doxygen.py
@brief  create doxygen documentation for project
********************************************************************************
"""

# autopep8: off
import sys
import os
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from Source.version import __title__, __version__, __description__, __author__  # pylint: disable=wrong-import-position
from Source.Util.app_data import S_ICON_RESOURCE_PATH, S_ICON_32_RESOURCE_PATH  # pylint: disable=wrong-import-position
from Source.Util.colored_log import init_console_logging  # pylint: disable=wrong-import-position
from Documentation.DoxygenCreator.doxygen_creator import DoxygenCreator, get_cmd_args, S_MAIN_FOLDER_FOLDER, S_PYTHON_PATTERN  # pylint: disable=wrong-import-position
# autopep8: on

init_console_logging(logging.INFO)

S_REPO_LINK = "https://github.com/timounger/YouTubeDownloader"


if __name__ == "__main__":
    args = get_cmd_args()
    doxygen_creator = DoxygenCreator(S_REPO_LINK)
    doxygen_creator.set_configuration("PROJECT_NAME", __title__)
    doxygen_creator.set_configuration("PROJECT_NUMBER", __version__)
    doxygen_creator.set_configuration("PROJECT_BRIEF", __description__)
    doxygen_creator.set_configuration("PROJECT_LOGO", f"{S_MAIN_FOLDER_FOLDER}{S_ICON_RESOURCE_PATH}")
    doxygen_creator.set_configuration("PROJECT_ICON", f"{S_MAIN_FOLDER_FOLDER}{S_ICON_32_RESOURCE_PATH}")
    doxygen_creator.set_configuration("DOCSET_PUBLISHER_NAME", __author__)
    doxygen_creator.set_configuration("INPUT", S_MAIN_FOLDER_FOLDER)
    l_exclude_pattern = [".env"]
    doxygen_creator.set_configuration("EXCLUDE_PATTERNS", l_exclude_pattern)
    l_file_pattern = [S_PYTHON_PATTERN, "*.md", "*.bat", "*.pyproject", "*.iss", "*.yml", "*.txt"]
    doxygen_creator.set_configuration("FILE_PATTERNS", l_file_pattern)
    sys.exit(doxygen_creator.run_doxygen(b_open_doxygen_output=args.open))
