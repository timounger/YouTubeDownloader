"""!
********************************************************************************
@file   doxygen_creator.py
@brief  create doxygen documentation
********************************************************************************
"""

import os
import logging
import difflib
import subprocess
import webbrowser
import time
import argparse
import zipfile
from typing import Any, Optional
from threading import Thread
from difflib import get_close_matches
import requests
import packaging.version

from Documentation.DoxygenCreator.configParser import ConfigParser

B_PLANTUML_SUPPORT = True
B_GITHUB_CORNER_SUPPORT = True
B_DOXY_CONFIG_DIFF_SUPPORT = True
B_DOXY_PY_CHECKER_SUPPORT = True
B_AUTO_VERSION_SUPPORT = True
B_FOOTER_SUPPORT = False

if B_DOXY_PY_CHECKER_SUPPORT:
    from Documentation.DoxygenCreator.doxy_py_checker import DoxyPyChecker  # pylint: disable=wrong-import-position

log = logging.getLogger("DoxygenCreator")

YES = "YES"
NO = "NO"
WARNING_FAIL = "FAIL_ON_WARNINGS"

S_DOXYGEN_PATH = "doxygen.exe"  # required: add doxygen bin path to file path in system variables
S_DEFAULT_OUTPUT_FOLDER = "Output_Doxygen"

S_MAIN_FOLDER_FOLDER = "../../"

DOXYGEN_VERSION = "1.14.0"
S_DOXYGEN_URL = f"https://sourceforge.net/projects/doxygen/files/rel-{DOXYGEN_VERSION}/doxygen-{DOXYGEN_VERSION}.windows.x64.bin.zip/download"
S_DOXYGEN_ZIP = f"doxygen-{DOXYGEN_VERSION}.windows.x64.bin.zip"
S_DOXYGEN_DLL = "libclang.dll"

S_WARNING_FILE_PREFIX = "Doxygen_warnings_"
S_WARNING_FILE_SUFFIX = ".log"
S_INDEX_FILE = "html/index.html"
I_TIMEOUT = 5  # timeout for tool download

S_PYTHON_PATTERN = "*.py"
L_DEFAULT_FILE_PATTERN: list[str] = []

if B_PLANTUML_SUPPORT:
    PLANT_UML_VERSION = "1.2025.7"
    S_PLANTUML_JAR_URL = f"https://github.com/plantuml/plantuml/releases/download/v{PLANT_UML_VERSION}/plantuml-{PLANT_UML_VERSION}.jar"
    S_PLANTUML_JAR_NAME = "plantuml.jar"
    S_PLANTUML_PATH = "./"  # need plantuml.jar in this folder
else:
    S_PLANTUML_PATH = ""

if B_DOXY_CONFIG_DIFF_SUPPORT:
    S_DOXY_DIFF_HTML_NAME = "DoxyfileDiff.html"
    S_DOXY_FILE_DEFAULT_NAME = "Default.Doxyfile"
    I_WRAP_LENGTH = 100

if B_GITHUB_CORNER_SUPPORT:
    S_GITHUB_CORNER_FIRST = "<a href="
    S_GITHUB_CORNER_LAST = """ class="github-corner" aria-label="View source on GitHub"><svg width="80" height="80" viewBox="0 0 250 250" style="fill:#151513; color:#fff; position: absolute; top: 0; border: 0; right: 0;" aria-hidden="true"><path d="M0,0 L115,115 L130,115 L142,142 L250,250 L250,0 Z"></path><path d="M128.3,109.0 C113.8,99.7 119.0,89.6 119.0,89.6 C122.0,82.7 120.5,78.6 120.5,78.6 C119.2,72.0 123.4,76.3 123.4,76.3 C127.3,80.9 125.5,87.3 125.5,87.3 C122.9,97.6 130.6,101.9 134.4,103.2" fill="currentColor" style="transform-origin: 130px 106px;" class="octo-arm"></path><path d="M115.0,115.0 C114.9,115.1 118.7,116.5 119.8,115.4 L133.7,101.6 C136.9,99.2 139.9,98.4 142.2,98.6 C133.8,88.0 127.5,74.4 143.8,58.0 C148.5,53.4 154.0,51.2 159.7,51.0 C160.3,49.4 163.2,43.6 171.4,40.1 C171.4,40.1 176.1,42.5 178.8,56.2 C183.1,58.6 187.2,61.8 190.9,65.4 C194.5,69.0 197.7,73.2 200.1,77.6 C213.8,80.2 216.3,84.9 216.3,84.9 C212.7,93.1 206.9,96.0 205.4,96.6 C205.1,102.4 203.0,107.8 198.3,112.5 C181.9,128.9 168.3,122.5 157.7,114.1 C157.9,116.9 156.7,120.9 152.7,124.9 L141.0,136.5 C139.8,137.7 141.6,141.9 141.8,141.8 Z" fill="currentColor" class="octo-body"></path></svg></a><style>.github-corner:hover .octo-arm{animation:octocat-wave 560ms ease-in-out}@keyframes octocat-wave{0%,100%{transform:rotate(0)}20%,60%{transform:rotate(-25deg)}40%,80%{transform:rotate(10deg)}}@media (max-width:500px){.github-corner:hover .octo-arm{animation:none}.github-corner .octo-arm{animation:octocat-wave 560ms ease-in-out}}</style>"""


class OpenNotepad(Thread):
    """!
    @brief Class to open Notepad in thread to prevent program stop until close file
    @param s_file : file to open
    """

    def __init__(self, s_file: str):
        Thread.__init__(self)
        self.s_file = s_file
        self.start()

    def run(self) -> None:
        """!
        @brief Open file with notepad
        """
        time.sleep(1)
        with subprocess.Popen(["notepad.exe", self.s_file]):
            pass


class DoxygenCreator():
    """!
    @brief Class to generate Doxygen documentation for any code documentation with uniform settings and styling.
    @param s_webside : URL to website
    """
    d_settings: dict[str, str | list[str] | int] = {
        "PROJECT_NAME": "MyProject",  # important to define default user name to create output folder and files
        "OUTPUT_DIRECTORY": S_DEFAULT_OUTPUT_FOLDER,
        "ABBREVIATE_BRIEF": "",  # Each string in this list, will be stripped from the text ("" to prevent warning)
        "FULL_PATH_NAMES": NO,
        "JAVADOC_AUTOBRIEF": YES,  # first line (until the first dot) of a Javadoc-style comment as the brief description
        "OPTIMIZE_OUTPUT_JAVA": YES,
        "TIMESTAMP": YES,
        "EXTRACT_ALL": YES,
        "INTERNAL_DOCS": YES,  # documentation after internal command is included
        "HIDE_SCOPE_NAMES": YES,  # full class and namespace scopes in the documentation
        "SORT_BRIEF_DOCS": YES,  # sort the brief descriptions of file namespace and class members alphabetically by member name
        "SORT_BY_SCOPE_NAME": YES,
        "WARN_NO_PARAMDOC": YES,
        "WARN_AS_ERROR": WARNING_FAIL,
        "INPUT": ["."],
        "FILE_PATTERNS": L_DEFAULT_FILE_PATTERN,
        "RECURSIVE": YES,
        "IMAGE_PATH": S_MAIN_FOLDER_FOLDER,
        "USE_MDFILE_AS_MAINPAGE": f"{S_MAIN_FOLDER_FOLDER}README.md",
        "SOURCE_BROWSER": YES,
        "INLINE_SOURCES": YES,
        "HTML_COLORSTYLE": "LIGHT",  # required with Doxygen >= 1.9.5
        "HTML_COLORSTYLE_HUE": 209,  # required for Doxygen Awesome
        "HTML_COLORSTYLE_SAT": 255,  # required for Doxygen Awesome
        "HTML_COLORSTYLE_GAMMA": 113,  # required for Doxygen Awesome
        "HTML_DYNAMIC_SECTIONS": YES,
        "HTML_COPY_CLIPBOARD": NO,  # required for Doxygen Awesome
        "DISABLE_INDEX": NO,  # required for Doxygen Awesome
        "GENERATE_TREEVIEW": YES,  # required for Doxygen Awesome
        "FULL_SIDEBAR": NO,  # required for Doxygen Awesome
        "SEARCHENGINE": YES,
        "SERVER_BASED_SEARCH": NO,
        "EXTERNAL_SEARCH": NO,
        "GENERATE_LATEX": NO,
        "LATEX_CMD_NAME": "latex",
        "UML_LOOK": YES,
        "DOT_IMAGE_FORMAT": "svg",
        "INTERACTIVE_SVG": YES,
        "PLANTUML_JAR_PATH": S_PLANTUML_PATH,
        "PLANTUML_INCLUDE_PATH": S_PLANTUML_PATH,
        "DOT_MULTI_TARGETS": YES,
        "DOT_CLEANUP": YES,
    }

    def __init__(self, s_webside: Optional[str] = None) -> None:
        self.s_webside = s_webside
        self.l_warnings: list[str] = []
        self.s_output_dir = ""
        self.s_doxyfile_name = ""
        self.s_warning_name = ""

    def create_default_doxyfile(self, s_file_name: str) -> None:
        """!
        @brief Create default doxyfile
        @param s_file_name : doxygen file name
        """
        subprocess.call([S_DOXYGEN_PATH, "-g", s_file_name])

    def set_configuration(self, s_type: str, value: Any, b_override: bool = True) -> None:
        """!
        @brief Set doxygen configuration.
        @param s_type : type to set in configuration
        @param value : value to set for s_type in configuration
        @param b_override : info if selected default setting should override
        """
        if isinstance(value, list):
            if b_override or (s_type not in self.d_settings):
                self.d_settings[s_type] = []
            list_to_extend = self.d_settings[s_type]  # Now mypy knows this is a list
            if isinstance(list_to_extend, list):
                list_to_extend.extend(value)
            else:
                log.warning("Not possible to append value to %s", s_type)
        else:
            if b_override or (s_type not in self.d_settings):
                self.d_settings[s_type] = value

    def get_configuration(self, s_type: str) -> Any:
        """!
        @brief Get type in doxygen configuration.
        @param s_type : type in configuration get setting
        @return configuration settings
        """
        if s_type in self.d_settings:
            value = self.d_settings[s_type]
        else:
            value = None  # is default value
        return value

    def prepare_doxyfile_configuration(self) -> None:
        """!
        @brief Prepare doxfile configuration with default settings that depend on other parameters.
               Parameters that set before as fix parameter or by user will not override.
               This allows the user to make settings that differ from the default configuration.
        """
        # set filenames and directories needed to save/open files
        self.s_output_dir = self.get_configuration('OUTPUT_DIRECTORY')  # save output directory witch used for other file names
        s_project_name = self.get_configuration("PROJECT_NAME")
        self.s_doxyfile_name = os.path.join(self.s_output_dir, f"{s_project_name}.Doxyfile")
        self.s_warning_name = os.path.join(self.s_output_dir, f"{S_WARNING_FILE_PREFIX}{s_project_name}{S_WARNING_FILE_SUFFIX}")

        # set uniform doxygen configuration that depend on other parameters
        self.set_configuration("PROJECT_BRIEF", f"{s_project_name}-Documentation", b_override=False)  # use project name as default if nothing defined
        self.set_configuration("WARN_LOGFILE", self.s_warning_name, b_override=False)
        self.set_configuration("EXCLUDE_PATTERNS", [self.s_output_dir], b_override=False)

        if B_AUTO_VERSION_SUPPORT:
            # write version prefix for version numbers as project number
            s_version = self.get_configuration("PROJECT_NUMBER")
            if s_version:
                try:
                    packaging.version.Version(s_version)  # test if s_sersion is a valid versions string
                    self.set_configuration("PROJECT_NUMBER", f"v{s_version}")
                except packaging.version.InvalidVersion:
                    pass  # not a valid version, do not prefix with "v"

        # set doxygen awesome settings witch depends on path
        l_extra_files = ["doxygen-awesome-darkmode-toggle.js",
                         "doxygen-awesome-fragment-copy-button.js",
                         "doxygen-awesome-paragraph-link.js",
                         "doxygen-awesome-interactive-toc.js",
                         "doxygen-awesome-tabs.js"]
        self.set_configuration("HTML_EXTRA_FILES", l_extra_files, b_override=False)
        l_extra_stylesheet = ["doxygen-awesome.css",
                              "doxygen-awesome-sidebar-only.css",
                              "doxygen-awesome-sidebar-only-darkmode-toggle.css"]
        self.set_configuration("HTML_EXTRA_STYLESHEET", l_extra_stylesheet, b_override=False)  # doxygen styling code
        self.set_configuration("HTML_HEADER", "header.html", b_override=False)  # use own doxygen header
        if B_FOOTER_SUPPORT:
            self.set_configuration("HTML_FOOTER", "footer.html", b_override=False)  # use own doxygen footer

    def edit_select_doxyfile_settings(self) -> None:
        """!
        @brief Override default settings in doxyfile with selected settings.
        """
        # load the default doxygen template file
        config_parser = ConfigParser()
        configuration = config_parser.load_configuration(self.s_doxyfile_name)
        l_existing_keys = list(configuration.keys())

        # write doxygen settings
        for key, value in self.d_settings.items():
            if key in l_existing_keys:
                if isinstance(value, list):
                    new_values = []
                    for entry in value:
                        new_values.append(entry)
                    configuration[key] = new_values
                else:
                    if isinstance(value, int):
                        value = str(value)  # integer can only write as string to doxyfile
                    configuration[key] = value
            else:
                text = f"'{key}' is a invalid doxygen setting"
                similar_key = get_close_matches(key, l_existing_keys, n=1)
                if len(similar_key) > 0:
                    text += f". Did you mean: '{similar_key[0]}'?"
                self.l_warnings.append(text)

        # store the configuration in doxyfile
        config_parser.store_configuration(configuration, self.s_doxyfile_name)

    def add_warnings(self) -> None:
        """!
        @brief Add warnings to warning file
        """
        if self.l_warnings:
            with open(self.s_warning_name, mode="a", encoding="utf-8") as file:
                for s_warning in self.l_warnings:
                    file.write(s_warning + "\n")

    if B_PLANTUML_SUPPORT:
        def download_plantuml_jar(self) -> None:
            """!
            @brief Download PlantUML Jar
            """
            if not os.path.exists(S_PLANTUML_JAR_NAME):
                log.info("Download %s ...", S_PLANTUML_JAR_NAME)
                try:
                    with requests.get(S_PLANTUML_JAR_URL, timeout=I_TIMEOUT) as response:
                        response.raise_for_status()
                        with open(S_PLANTUML_JAR_NAME, mode="wb") as file:  # download plantuml.jar
                            file.write(response.content)  # download plantuml.jar
                except requests.Timeout:
                    log.error("Timeout for download %s!", S_PLANTUML_JAR_NAME)
                except requests.RequestException as e:
                    log.error("Can not download %s! %s", S_PLANTUML_JAR_NAME, e)
            else:
                log.info("%s already exist!", S_PLANTUML_JAR_NAME)

    def download_doxygen(self) -> None:
        """!
        @brief Download Doxygen
        """
        if not os.path.exists(S_DOXYGEN_PATH) or not os.path.exists(S_DOXYGEN_DLL):
            if not os.path.exists(S_DOXYGEN_ZIP):
                log.info("Download %s ...", S_DOXYGEN_ZIP)
                try:
                    with requests.get(S_DOXYGEN_URL, timeout=I_TIMEOUT) as response:
                        response.raise_for_status()
                        with open(S_DOXYGEN_ZIP, mode="wb") as file:  # download doxygen
                            file.write(response.content)
                except requests.Timeout:
                    log.error("Timeout for download %s!", S_DOXYGEN_ZIP)
                except requests.RequestException as e:
                    log.error("Can not download %s! %s", S_DOXYGEN_ZIP, e)
            else:
                log.info("%s already exist!", S_DOXYGEN_ZIP)
            with zipfile.ZipFile(S_DOXYGEN_ZIP, mode="r") as zip_ref:
                zip_ref.extract(S_DOXYGEN_PATH, "./")
                zip_ref.extract(S_DOXYGEN_DLL, "./")
        else:
            log.info("%s and %s already exist!", S_DOXYGEN_PATH, S_DOXYGEN_DLL)

    def check_doxygen_warnings(self, b_open_warning_file: bool = True) -> bool:
        """!
        @brief Check for doxygen Warnings
        @param b_open_warning_file : [True] open warning file; [False] only check for warnings
        @return status if doxygen warnings exist
        """
        b_warnings = False

        if os.path.exists(self.s_warning_name):
            with open(self.s_warning_name, mode="r", encoding="utf-8") as file:
                lines = file.readlines()
                if len(lines) != 0:
                    b_warnings = True
                    log.warning("Doxygen Warnings found!!!")
                    for s_line in lines:
                        log.warning("  %s", s_line)

        if b_open_warning_file and b_warnings:
            OpenNotepad(self.s_warning_name)

        return b_warnings

    def generate_doxygen_output(self, b_open_doxygen_output: bool = True) -> None:
        """!
        @brief Generate Doxygen output depend on existing doxyfile
        @param b_open_doxygen_output : [True] open output in browser; [False] only generate output
        """
        subprocess.call([S_DOXYGEN_PATH, self.s_doxyfile_name])

        if b_open_doxygen_output:
            # open doxygen output
            filename = f"file:///{os.getcwd()}/{self.s_output_dir}/{S_INDEX_FILE}"
            webbrowser.open_new_tab(filename)

    if B_GITHUB_CORNER_SUPPORT:
        def add_github_corner(self) -> None:
            """!
            @brief Add Github corner and tab icon
            """
            s_folder = f"{self.s_output_dir}/html/"
            if self.s_webside is not None:
                s_corner_text = S_GITHUB_CORNER_FIRST + self.s_webside + S_GITHUB_CORNER_LAST
            else:
                s_corner_text = None
            for html_file in os.listdir(s_folder):
                if html_file.endswith(".html"):
                    file_path = f"{s_folder}{html_file}"
                    with open(file_path, mode="a", encoding="utf-8") as file:
                        if s_corner_text is not None:
                            file.write(s_corner_text + "\n")

    def add_nojekyll_file(self) -> None:
        """!
        @brief Add .nojekyll file that files with underscores visible
        """
        s_file_name = ".nojekyll"
        with open(f"{self.s_output_dir}/html/{s_file_name}", mode="w", encoding="utf-8") as file:
            file.write("")

    if B_DOXY_CONFIG_DIFF_SUPPORT:
        def generate_configuration_diff(self) -> None:
            """!
            @brief Generate doxyfile diff to view changes
            """
            s_default_doxyfile = os.path.join(self.s_output_dir, S_DOXY_FILE_DEFAULT_NAME)

            # create and read default doxyfile
            self.create_default_doxyfile(s_default_doxyfile)
            config_parser = ConfigParser()
            configuration = config_parser.load_configuration(s_default_doxyfile)
            config_parser.store_configuration(configuration, s_default_doxyfile)
            with open(s_default_doxyfile, mode="r", encoding="utf-8") as file:
                s_default_config = file.read()
            os.remove(s_default_doxyfile)

            # read modified doxyfile
            with open(self.s_doxyfile_name, mode="r", encoding="utf-8") as file:
                s_modified_config = file.read()

            s_diff_file_name = os.path.join(self.s_output_dir, S_DOXY_DIFF_HTML_NAME)
            difference = difflib.HtmlDiff(wrapcolumn=I_WRAP_LENGTH).make_file(s_default_config.splitlines(), s_modified_config.splitlines(), "Default", "Modified")
            with open(s_diff_file_name, mode="w", encoding="utf-8") as file:
                file.write(difference)

    def run_doxygen(self, b_open_doxygen_output: bool = True) -> bool:
        """!
        @brief Generate Doxyfile and Doxygen output depend on doxyfile settings
        @param b_open_doxygen_output : [True] open output in browser; [False] only generate output
        @return status for found doxygen warning
        """
        self.download_doxygen()
        if B_PLANTUML_SUPPORT:
            self.download_plantuml_jar()
        self.prepare_doxyfile_configuration()
        if not os.path.exists(self.s_output_dir):
            os.makedirs(self.s_output_dir)
        self.create_default_doxyfile(self.s_doxyfile_name)
        self.edit_select_doxyfile_settings()
        self.generate_doxygen_output(b_open_doxygen_output)
        if B_GITHUB_CORNER_SUPPORT:
            self.add_github_corner()
        self.add_nojekyll_file()
        if B_DOXY_CONFIG_DIFF_SUPPORT:
            self.generate_configuration_diff()

        if B_DOXY_PY_CHECKER_SUPPORT:
            # additional script to check for valid doxygen specification in python files
            file_patterns = self.d_settings["FILE_PATTERNS"]
            if isinstance(file_patterns, list):
                l_file_patterns = [str(pattern) for pattern in file_patterns]
            else:
                l_file_patterns = [str(file_patterns)]
            if S_PYTHON_PATTERN in l_file_patterns:
                doxy_checker = DoxyPyChecker(S_MAIN_FOLDER_FOLDER)
                l_finding = doxy_checker.run_check()
                self.l_warnings.extend(l_finding)

        self.add_warnings()  # add own warnings to warning file
        b_warnings = self.check_doxygen_warnings(b_open_doxygen_output)

        return b_warnings


def get_cmd_args() -> argparse.Namespace:
    """!
    @brief Function to define CMD arguments.
    @return Function returns argument parser.
    """
    o_parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    o_parser.add_argument("-o", "--open",
                          type=bool,
                          default=False,
                          help="open output files after generation")
    return o_parser.parse_args()
