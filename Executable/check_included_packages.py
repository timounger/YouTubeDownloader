"""!
********************************************************************************
@file   check_included_packages.py
@brief  Utility script to list and check if the build executable
        contains only specified third party packages
********************************************************************************
"""

import logging
import re
from bs4 import BeautifulSoup

from Source.version import __title__

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
    "pytube",
    # colored log
    "colorama"
]

S_RELATIVE_PATH = fr"build\{__title__}\xref-{__title__}.html"


def check_included_packages() -> list:
    """!
    @brief Check included packages
    @return status if included packages are okay
    """
    d_third_party = {}
    d_buildin = {}
    d_own_packs = {}

    # Regular Expressions
    regex_third_party = re.compile(r".env\/lib\/site-packages.*.py", re.IGNORECASE)
    regex_third_party_name = re.compile(r"(?<=site-packages\/).*", re.IGNORECASE)
    regex_builtin = re.compile(r".env\/lib\/.*.py", re.IGNORECASE)
    regex_builtin_name = re.compile(r"(?<=lib\/).*", re.IGNORECASE)
    regex_own_packs = re.compile(fr"{__title__}\/.*")

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
                matches = regex_third_party_name.search(s_package_path)
                if matches is not None:
                    d_third_party[matches.group().split("/", maxsplit=1)[0].replace(".py", "")] = ""
            elif regex_builtin.search(s_package_path):
                matches = regex_builtin_name.search(s_package_path)
                if matches is not None:
                    d_buildin[matches.group().replace(".py", "")] = ""
            elif regex_own_packs.search(s_package_path):
                matches = regex_own_packs.search(s_package_path)
                if matches is not None:
                    d_own_packs[matches.group()] = ""

    # print included packages
    log.debug("\nThird party packages:")
    log.debug("\n".join(list(d_third_party.keys())))
    log.debug("\nOwn packages:")
    log.debug("\n".join(list(d_own_packs.keys())))
    log.debug("\nPython buildin packages:")
    log.debug("\n".join(list(d_buildin.keys())))

    # check third party packages
    l_not_allowed_packages = []
    for s_package in list(d_third_party.keys()):
        if s_package not in L_ALLOWED_THIRD_PARTY_PACKAGES:
            l_not_allowed_packages.append(f"ERROR PyInstaller included an unknown package in the executable: \'{s_package}\'")
    return l_not_allowed_packages
