# This Python file uses the following encoding: utf-8
"""
*****************************************************************************
 @file    generate_executable.py
 @brief   Generate executable file
*****************************************************************************
"""

# autopep8: off
import sys
import os
import subprocess
import shutil
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Executable.generate_version_file import generate_version_file  # pylint: disable=wrong-import-position
from Executable.check_included_packages import check_included_packages  # pylint: disable=wrong-import-position

from Source.version import __title__  # pylint: disable=wrong-import-position
# autopep8: on

WORKPATH = "build"
VERSION_FILE_NAME = "downloader_version_info.txt"

L_EXCLUDE_MODULES = [
    # actual not used
    "moviepy",
]


add_data = [
    "..\\Resources\\YouTubeDownloader.ico;Resources\\"
]


hiddel_import = [
    "html.parser"
]


def get_type_list(type_name: str, l_type_values: List) -> List:
    """!
    @brief get type list
    @param type_name : type name
    @param l_type_values : type values
    @return type list
    """
    type_list = []
    for type_value in l_type_values:
        type_list.extend([f"--{type_name}", type_value])
    return type_list


WARNING_FILE = "PyInstaller_warnings.txt"

command = ["..\.env\Scripts\python", "-m", "PyInstaller", "--clean"]
command.extend(["--paths", "..\\"])
command.extend(get_type_list("add-data", add_data))
command.extend(["--icon", "..\\Resources\\YouTubeDownloader.ico"])
command.extend(["--version-file", f"{WORKPATH}\\{VERSION_FILE_NAME}"])
command.extend(get_type_list("hidden-import", hiddel_import))
command.extend(get_type_list("exclude-module", L_EXCLUDE_MODULES))
command.extend(["--name", __title__])
command.extend(["--onefile", "--noconsole", "--noupx",])
command.extend(["--distpath", "bin"])
command.extend(["--workpath", WORKPATH])
command.extend(["../Source/youtube_downloader.py"])

if __name__ == "__main__":
    result_report = []
    generate_version_file(VERSION_FILE_NAME, WORKPATH)
    result = subprocess.run(command, stderr=subprocess.PIPE, text=True, shell=True, check=False)
    if result.returncode != 0:
        result_report.append("Build executable failed!")
        result_report.append(result.stderr)
    else:
        build_warnings = [line for line in result.stderr.split("\n") if "WARNING" in line]
        if build_warnings:
            result_report.extend(build_warnings)
        else:
            l_not_allowed_packages = check_included_packages()
            if l_not_allowed_packages:
                result_report.extend(l_not_allowed_packages)
    print(result.stderr)
    with open(WARNING_FILE, mode="w", encoding="utf-8") as file:
        report = "\n".join(result_report)
        print(report)
        file.write(report)
    if result_report:
        print("FAILED build of executable")
        ret_value = 1
    else:
        s_spec_file = f"{__title__}.spec"
        if os.path.exists(s_spec_file):
            os.remove(s_spec_file)
        if os.path.exists(WORKPATH):
            shutil.rmtree(WORKPATH)
        print("SUCCESS build of executable")
        ret_value = 0
    sys.exit(ret_value)
