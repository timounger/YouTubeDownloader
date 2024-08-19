# This Python file uses the following encoding: utf-8
"""
*****************************************************************************
 @file    check_included_packages.py
 @brief   Utility script to list and check if the build executable
          contains only specified third party packages
*****************************************************************************
"""

import sys
import logging
import re
from typing import List
from bs4 import BeautifulSoup

log = logging.getLogger("CheckIncludedPackages")

# List of third party packages that may be contained in the PyInstaller executable.
# Has to be manually extended if a new package gets added to the tool.
L_ALLOWED_THIRD_PARTY_PACKAGES = [
    # not possible to exclude
    "PyInstaller",
    # clipboard
    "clipboard",
    "pyperclip",
    # youtube downloader
    "pytube"
]

APP_NAME = "YouTubeDownloader"

S_RELATIVE_PATH = fr"build\{APP_NAME}\xref-{APP_NAME}.html"


def check_included_packages() -> List:
    """!
    @brief Check included packages
    @return status if included packages are okay
    """
    d_third_party = {}
    d_buildin = {}
    d_own_packs = {}

    # Regular Expressions
    regex_third_party = re.compile(r"Python[0-9]*\/lib\/site-packages.*.py", re.IGNORECASE)
    regex_third_party_name = re.compile(r"(?<=site-packages\/).*", re.IGNORECASE)
    regex_builtin = re.compile(r"Python[0-9]*\/lib\/.*.py", re.IGNORECASE)
    regex_builtin_name = re.compile(r"(?<=lib\/).*", re.IGNORECASE)
    regex_own_packs = re.compile(fr"{APP_NAME}\/.*")

    # read PyInstaller modulegraph cross reference HTML
    with open(S_RELATIVE_PATH, mode="r", encoding="utf-8") as o_html_file:
        soup = BeautifulSoup(o_html_file, "html.parser")

    # parse HTML
    l_nodes = soup.find_all("div", class_="node")
    for o_node in l_nodes:
        l_targets = o_node.find_all("a", target="code")
        for o_target in l_targets:
            s_package_path = o_target["href"]
            if regex_third_party.search(s_package_path):
                d_third_party[regex_third_party_name.search(s_package_path).group().split("/", maxsplit=1)[0].replace(".py", "")] = ""
            elif regex_builtin.search(s_package_path):
                d_buildin[regex_builtin_name.search(s_package_path).group().replace(".py", "")] = ""
            elif regex_own_packs.search(s_package_path):
                d_own_packs[regex_own_packs.search(s_package_path).group()] = ""

    # print included packages
    log.info("\nThird party packages:")
    log.info("\n".join(list(d_third_party.keys())))
    # log.info("\nOwn packages:")
    # log.info("\n".join(list(d_own_packs.keys())))
    # log.info("\nPython buildin packages:")
    # log.info("\n".join(list(d_buildin.keys())))

    # check third party packages
    l_not_allowed_packages = []
    for s_package in list(d_third_party.keys()):
        if s_package not in L_ALLOWED_THIRD_PARTY_PACKAGES:
            l_not_allowed_packages.append(f"ERROR PyInstaller included an unknown package in the executable: \'{s_package}\'")
    return l_not_allowed_packages


if __name__ == "__main__":
    sys.exit(check_included_packages())
