"""!
********************************************************************************
@file   generate_executable.py
@brief  Generate executable file
********************************************************************************
"""

# autopep8: off
import sys
import os
import logging
import subprocess
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Executable.generate_git_version import generate_git_version_file  # pylint: disable=wrong-import-position
from Executable.generate_version_file import generate_version_file  # pylint: disable=wrong-import-position
from Executable.check_included_packages import check_included_packages  # pylint: disable=wrong-import-position

from Source.version import __title__  # pylint: disable=wrong-import-position
from Source.Util.colored_log import init_console_logging  # pylint: disable=wrong-import-position
# autopep8: on

log = logging.getLogger("GenerateExecutable")
init_console_logging(logging.INFO)

WORKPATH = "build"
GIT_VERSION_PATH = "../Source/Util"
VERSION_FILE_NAME = "version_info.txt"
WARNING_FILE = "PyInstaller_warnings.txt"

L_EXCLUDE_MODULES = [
    "PIL",
    "charset_normalizer",
    "numpy",
    "pkg_resources",
    "typing_extensions",
    "darkdetect._mac_detect",
    # actual not used
    "moviepy",
]

TOLERATED_WARNINGS = [
    "No backend available"  # possible on CI
]

add_data = [
    "..\\Resources\\app.ico;Resources\\"
]


L_HIDDEN_IMPORT = [
    "html.parser"
]


def get_type_list(type_name: str, l_type_values: list[str]) -> list[str]:
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


if __name__ == "__main__":
    result_report = []

    command = [r"..\.env\Scripts\python", "-m", "PyInstaller", "--clean"]
    command.extend(["--paths", "..\\"])
    command.extend(get_type_list("add-data", add_data))
    command.extend(["--icon", "..\\Resources\\app.ico"])
    command.extend(["--version-file", f"{WORKPATH}\\{VERSION_FILE_NAME}"])
    command.extend(get_type_list("hidden-import", L_HIDDEN_IMPORT))
    command.extend(get_type_list("exclude-module", L_EXCLUDE_MODULES))
    command.extend(["--name", __title__])
    command.extend(["--onefile", "--noconsole", "--noupx",])
    command.extend(["--distpath", "bin"])
    command.extend(["--workpath", WORKPATH])
    command.extend(["../Source/app.py"])

    generate_git_version_file(GIT_VERSION_PATH)
    generate_version_file(VERSION_FILE_NAME, WORKPATH)

    result = subprocess.run(command, stderr=subprocess.PIPE, text=True, shell=True, check=False)
    if result.returncode != 0:
        result_report.append("Build executable failed!")
        result_report.append(result.stderr)
    else:
        possible_build_warnings = [line for line in result.stderr.split("\n") if "WARNING" in line]
        build_warnings = []
        for warning in possible_build_warnings:
            b_tolerate = False
            for tolerate in TOLERATED_WARNINGS:
                if tolerate in warning:
                    b_tolerate = True
                    break
            if not b_tolerate:
                build_warnings.append(warning)
        if build_warnings:
            result_report.extend(build_warnings)
        else:
            l_not_allowed_packages = check_included_packages()
            if l_not_allowed_packages:
                result_report.extend(l_not_allowed_packages)
    log.info(result.stderr)

    with open(WARNING_FILE, mode="w", encoding="utf-8") as file:
        report = "\n".join(result_report)
        if report:
            log.warning(report)
        file.write(report)
    if result_report:
        log.error("FAILED build of executable")
        ret_value = 1
    else:
        s_spec_file = f"{__title__}.spec"
        if os.path.exists(s_spec_file):
            os.remove(s_spec_file)
        if os.path.exists(WORKPATH):
            shutil.rmtree(WORKPATH)
        log.info("SUCCESS build of executable")
        ret_value = 0
    sys.exit(ret_value)
