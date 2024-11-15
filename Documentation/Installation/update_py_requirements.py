"""!
********************************************************************************
@file   update_py_requirements.py
@brief  Update version in requirement files
********************************************************************************
"""

# autopep8: off
import sys
import os
import logging
import re
from typing import NamedTuple
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from Source.Util.colored_log import init_console_logging  # pylint: disable=wrong-import-position
from Source.Util.openpyxl_util import XLSCreator  # pylint: disable=wrong-import-position
# autopep8: on

log = logging.getLogger("UpdatePyRequirements")
init_console_logging(logging.INFO)

L_FILES = ["requirements.txt", "constraints.txt"]  # files to update
L_IGNORE_PACKAGES: list[str] = []
FONT_NAME = "Consolas"
I_TIMEOUT = 2  # timeout to get pip data

L_PACKAGE_INFO_TITLE = ["Package", "Version", "Author", "Author_Mail", "License", "Homepage", "Package URL", "Requires", "Requires Py"]


class PackageInfo(NamedTuple):
    """!
    @brief Package Information.
    """
    package: str
    version: int
    author: str
    author_mail: str
    license_info: str
    home_page: str
    package_url: str
    requires_dist: list[str]
    requires_py: str


def create_package_summary_xls(l_package_info: list[PackageInfo]) -> None:
    """!
    @brief Update xls field with package summary
    @param l_package_info : list with package infos
    """
    xls_creator = XLSCreator(font_name=FONT_NAME)
    worksheet = xls_creator.workbook.active
    worksheet.title = "PackageInfo"
    for i, title in enumerate(L_PACKAGE_INFO_TITLE):
        xls_creator.set_cell(worksheet, 1, i + 1, title, bold=True)
    l_added_package = []
    i_package = 0
    for package in l_package_info:
        if package not in l_added_package:
            l_added_package.append(package)
            for i, value in enumerate(package):
                if isinstance(value, list):
                    if not value:
                        value = ""
                    else:
                        value = "\n".join(value)
                elif isinstance(value, str):
                    pass
                elif not value:
                    value = ""
                xls_creator.set_cell(worksheet, i_package + 2, i + 1, str(value))
            i_package += 1
    xls_creator.set_table(worksheet, max_col=len(l_added_package[0]), max_row=len(l_added_package) + 1)
    xls_creator.set_column_autowidth(worksheet)
    worksheet.freeze_panes = "C2"
    xls_creator.save(filename="PackageInfos.xlsx")
    log.info("Write %s package infos to file", len(l_added_package))


def get_package_info(package: str) -> PackageInfo | None:
    """!
    @brief Upgrade package from text file to latest version
    @param package : check latest version of this package
    @return package info
    """
    try:
        url = f"https://pypi.org/pypi/{package}/json"
        response = requests.get(url, timeout=I_TIMEOUT)
        response.raise_for_status()
        d_package_info = response.json()
    except requests.exceptions.RequestException as e:
        log.error("Error occurred: %s", e)
        package_info = None
    else:
        l_requires_dist: list[str] = []
        requires_dist = d_package_info["info"]["requires_dist"]
        if requires_dist:
            for req in requires_dist:
                l_requires_dist.append(req)
        package_info = PackageInfo(package,
                                   d_package_info["info"]["version"],
                                   d_package_info["info"]["author"],
                                   d_package_info["info"]["author_email"],
                                   d_package_info["info"]["license"],
                                   d_package_info["info"]["home_page"],
                                   d_package_info["info"]["package_url"],
                                   l_requires_dist,
                                   d_package_info["info"]["requires_python"])
    return package_info


def update_packages(filename: str) -> list[PackageInfo]:
    """!
    @brief Update package from text file to latest version
    @param filename : file name
    @return list with updated packages
    """
    with open(filename, mode="r", encoding="utf-8") as file:
        lines = file.readlines()

    i_update_cnt = 0
    l_package_info = []
    updated_lines = []
    for line in lines:
        if re.match(r"^\s*#", line):  # comment line
            updated_lines.append(line)
        elif re.match(r"^\s*([\w\-]+)==([\w\.\-]+)\s*(#.*)?$", line):  # check for fix version 'package==version'
            package, version, comment = re.findall(r"^\s*([\w\-]+)==([\w\.\-]+)\s*(#.*)?$", line)[0]
            if comment != "":
                comment = f" {comment}"
            package_info = get_package_info(package)
            if (package_info is not None) and (package not in L_IGNORE_PACKAGES):
                if package_info.version and (package_info.version != version):
                    updated_lines.append(f"{package}=={package_info.version}{comment}\n")
                    i_update_cnt += 1
                    log.info("Updated: %s %s", package, package_info.version)
                else:
                    updated_lines.append(line)
                    log.debug(line)
                l_package_info.append(package_info)
            else:
                updated_lines.append(line)
                log.debug(line)
        else:  # package without version
            updated_lines.append(line)
            if line.strip():
                package_info = get_package_info(line)
                if package_info is not None:
                    l_package_info.append(package_info)
                    log.debug(line)

    with open(filename, mode="w", encoding="utf-8") as file:
        file.writelines(updated_lines)
        log.info("%s packages updates in %s\n", i_update_cnt, filename)
    return l_package_info


if __name__ == "__main__":
    l_all_package_info = []
    for req_file in L_FILES:
        l_file_package = update_packages(req_file)
        l_all_package_info += l_file_package
    if l_all_package_info:
        create_package_summary_xls(l_all_package_info)
    log.info("All packages checked and updated!")
