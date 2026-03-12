"""!
********************************************************************************
@file   check_included_packages.py
@brief  Utility script to list and check if the build executable
        contains only specified third party packages.
********************************************************************************
"""

import logging
import re
from bs4 import BeautifulSoup

from Source.version import __title__

log = logging.getLogger("CheckIncludedPackages")

# List of third party packages that may be contained in the PyInstaller executable.
# Has to be manually extended if a new package gets added to the tool.
ALLOWED_THIRD_PARTY_PACKAGES = [
    # not possible to exclude
    "PyInstaller",
    # clipboard
    "clipboard",
    "pyperclip",
    # youtube downloader
    "pytubefix",
    "customtkinter",
    "darkdetect",
    "packaging",
    "openpyxl",
    "et_xmlfile",
    "aiohappyeyeballs",
    "aiohttp",
    "aiosignal",
    "attr",
    "frozenlist",
    "idna",
    "multidict",
    "propcache",
    "yarl",
    "typing_extensions",
    "nodejs_wheel",
    # colored log
    "colorama"
]

RELATIVE_PATH = fr"build\{__title__}\xref-{__title__}.html"


def check_included_packages() -> list[str]:
    """!
    @brief Parse PyInstaller cross-reference HTML and verify all third-party packages are whitelisted.
    @return list of error messages for unknown packages (empty if all packages are allowed)
    """
    third_party: set[str] = set()
    builtin: set[str] = set()
    own_packs: set[str] = set()

    # Regular Expressions
    regex_third_party = re.compile(r"\.venv\/lib\/site-packages.*.py", re.IGNORECASE)
    regex_third_party_name = re.compile(r"(?<=site-packages\/).*", re.IGNORECASE)
    regex_builtin = re.compile(r"\.venv\/lib\/.*.py", re.IGNORECASE)
    regex_builtin_name = re.compile(r"(?<=lib\/).*", re.IGNORECASE)
    regex_own_packs = re.compile(fr"{__title__}\/.*")

    # read PyInstaller modulegraph cross reference HTML
    with open(RELATIVE_PATH, mode="r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, "html.parser")

    # parse HTML
    nodes = soup.find_all("div", class_="node")
    for node in nodes:
        targets = node.find_all("a", target="code")
        for target in targets:
            package_path = target["href"]
            if regex_third_party.search(package_path):
                matches = regex_third_party_name.search(package_path)
                if matches is not None:
                    third_party.add(matches.group().split("/", maxsplit=1)[0].replace(".py", ""))
            elif regex_builtin.search(package_path):
                matches = regex_builtin_name.search(package_path)
                if matches is not None:
                    builtin.add(matches.group().replace(".py", ""))
            else:
                matches = regex_own_packs.search(package_path)
                if matches is not None:
                    own_packs.add(matches.group())

    # print included packages
    log.debug("\nThird party packages:")
    log.debug("\n".join(sorted(third_party)))
    log.debug("\nOwn packages:")
    log.debug("\n".join(sorted(own_packs)))
    log.debug("\nPython builtin packages:")
    log.debug("\n".join(sorted(builtin)))

    # check third party packages
    return [f"ERROR PyInstaller included an unknown package in the executable: '{package}'"
            for package in third_party if package not in ALLOWED_THIRD_PARTY_PACKAGES]
