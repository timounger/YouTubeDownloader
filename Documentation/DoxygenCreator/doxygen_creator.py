# This Python file uses the following encoding: utf-8
"""
*****************************************************************************
 @file    doxygen_creator.py
 @brief   create doxygen documentation
*****************************************************************************
"""

import sys
import os
import difflib
import subprocess
import webbrowser
import time
import argparse
import shutil
import zipfile
from typing import Any
from threading import Thread
from doxygen import ConfigParser
import requests


# user include
sys.path.append('../../')
import Source.Util.downloader_data as mdata # pylint: disable=wrong-import-position
from Documentation.DoxygenCreator.doxy_py_checker import DoxyPyChecker # pylint: disable=wrong-import-position
from Source import version # pylint: disable=wrong-import-position

B_USE_OWN_STYLE = True
B_SIDEBAR_ONLY = True

S_DOXYGEN_PATH = "doxygen.exe" # required: add doxygen bin path to file path in system variables
S_DEFAULT_OUTPUT_FOLDER = "Output_Doxygen"
S_PUBLISHER = "Timo Unger"
S_MAIN_FOLDER_FOLDER = "../../"
S_PLANTUML_PATH = "./" # need plantuml.jar in this folder
S_PLANTUML_JAR_URL = "https://github.com/plantuml/plantuml/releases/download/v1.2023.8/plantuml-1.2023.8.jar"
S_PLANTUML_JAR_NAME = "plantuml.jar"
S_DOXYGEN_URL = "https://sourceforge.net/projects/doxygen/files/rel-1.9.7/doxygen-1.9.7.windows.x64.bin.zip/download"
S_DOXYGEN_ZIP = "doxygen-1.9.7.windows.x64.bin.zip"
S_DOXYGEN_DLL = "libclang.dll"
S_WARNING_FILE_PREFIX = "Doxygen_warnings_"
S_WARNING_FILE_SUFFIX = ".log"
S_INDEX_FILE = "html/index.html"
I_WRAP_LENGHT = 100
I_TIMEOUT = 5 # timeout for tool download

YES = "YES"
NO = "NO"
WARNING_FAIL = "FAIL_ON_WARNINGS"

S_PYTHON_PATTERN = '*.py'
L_DEFAULT_FILE_PATTERN = []

S_GITHUB_CORNER_FIRST = "<a href="
S_GITHUB_CORNER_LAST = """ class="github-corner" aria-label="View source on GitHub"><svg width="80" height="80" viewBox="0 0 250 250" style="fill:#151513; color:#fff; position: absolute; top: 0; border: 0; right: 0;" aria-hidden="true"><path d="M0,0 L115,115 L130,115 L142,142 L250,250 L250,0 Z"></path><path d="M128.3,109.0 C113.8,99.7 119.0,89.6 119.0,89.6 C122.0,82.7 120.5,78.6 120.5,78.6 C119.2,72.0 123.4,76.3 123.4,76.3 C127.3,80.9 125.5,87.3 125.5,87.3 C122.9,97.6 130.6,101.9 134.4,103.2" fill="currentColor" style="transform-origin: 130px 106px;" class="octo-arm"></path><path d="M115.0,115.0 C114.9,115.1 118.7,116.5 119.8,115.4 L133.7,101.6 C136.9,99.2 139.9,98.4 142.2,98.6 C133.8,88.0 127.5,74.4 143.8,58.0 C148.5,53.4 154.0,51.2 159.7,51.0 C160.3,49.4 163.2,43.6 171.4,40.1 C171.4,40.1 176.1,42.5 178.8,56.2 C183.1,58.6 187.2,61.8 190.9,65.4 C194.5,69.0 197.7,73.2 200.1,77.6 C213.8,80.2 216.3,84.9 216.3,84.9 C212.7,93.1 206.9,96.0 205.4,96.6 C205.1,102.4 203.0,107.8 198.3,112.5 C181.9,128.9 168.3,122.5 157.7,114.1 C157.9,116.9 156.7,120.9 152.7,124.9 L141.0,136.5 C139.8,137.7 141.6,141.9 141.8,141.8 Z" fill="currentColor" class="octo-body"></path></svg></a><style>.github-corner:hover .octo-arm{animation:octocat-wave 560ms ease-in-out}@keyframes octocat-wave{0%,100%{transform:rotate(0)}20%,60%{transform:rotate(-25deg)}40%,80%{transform:rotate(10deg)}}@media (max-width:500px){.github-corner:hover .octo-arm{animation:none}.github-corner .octo-arm{animation:octocat-wave 560ms ease-in-out}}</style>"""
S_ICON_FIRST = """<link rel="icon" type="image/x-icon" href="""
S_ICON_LAST = """>"""

S_REPO_LINK = "https://github.com/timounger/YouTubeDownloader"

S_DEFAULT = "_DEFAULT_KEY" # this values not set in doxyfile
S_AUTO = "_AUTO_KEY" # this values not set in doxyfile and you will get a warning if forget to override this value
L_OVERRIDE = [S_DEFAULT, S_AUTO] # this values are possible to override with global settings

class OpenNotepad(Thread):
    """!
    @brief  Class to open Notepad in thread to prevent program stop until close file
    @param  s_file : file to open
    """
    def __init__(self, s_file: str):
        Thread.__init__(self)
        self.s_file = s_file
        self.start()

    def run(self):
        """!
        @brief  Open file with notepad
        """
        time.sleep(1)
        with subprocess.Popen(["notepad.exe", self.s_file]):
            pass

class DoxygenCreator():
    """!
    @brief  Class to generate Doxygen documentation for any code documentation with uniform settings and styling.
    @param  s_webside : URL to website
    @param  s_logo : optional logo for webbrowser logo
    """
    d_settings =  {
        'DOXYFILE_ENCODING'       : S_DEFAULT, # UTF-8
        'PROJECT_NAME'            : "MyProject", # important to define default user name to create output folder and files
        'PROJECT_NUMBER'          : S_DEFAULT,
        'PROJECT_BRIEF'           : S_AUTO,
        'PROJECT_LOGO'            : S_AUTO,
        'OUTPUT_DIRECTORY'        : S_DEFAULT_OUTPUT_FOLDER,
        'CREATE_SUBDIRS'          : S_DEFAULT,
        'ALLOW_UNICODE_NAMES'     : S_DEFAULT,
        'OUTPUT_LANGUAGE'         : S_DEFAULT,
        'BRIEF_MEMBER_DESC'       : S_DEFAULT,
        'REPEAT_BRIEF'            : S_DEFAULT,
        'ABBREVIATE_BRIEF'        : "", # Each string in this list, will be stripped from the text ("" to prevent warning)
        'ALWAYS_DETAILED_SEC'     : S_DEFAULT,
        'INLINE_INHERITED_MEMB'   : S_DEFAULT,
        'FULL_PATH_NAMES'         : NO,
        'STRIP_FROM_PATH'         : S_DEFAULT,
        'STRIP_FROM_INC_PATH'     : S_DEFAULT,
        'SHORT_NAMES'             : S_DEFAULT,
        'JAVADOC_AUTOBRIEF'       : YES, # first line (until the first dot) of a Javadoc-style comment as the brief description
        'JAVADOC_BANNER'          : S_DEFAULT,
        'QT_AUTOBRIEF'            : S_DEFAULT,
        'MULTILINE_CPP_IS_BRIEF'  : S_DEFAULT,
        'PYTHON_DOCSTRING'        : S_DEFAULT,
        'INHERIT_DOCS'            : S_DEFAULT,
        'SEPARATE_MEMBER_PAGES'   : S_DEFAULT,
        'TAB_SIZE'                : S_DEFAULT,
        'ALIASES'                 : S_DEFAULT,
        'OPTIMIZE_OUTPUT_FOR_C'   : S_DEFAULT,
        'OPTIMIZE_OUTPUT_JAVA'    : YES,
        'OPTIMIZE_FOR_FORTRAN'    : S_DEFAULT,
        'OPTIMIZE_OUTPUT_VHDL'    : S_DEFAULT,
        'OPTIMIZE_OUTPUT_SLICE'   : S_DEFAULT,
        'EXTENSION_MAPPING'       : S_DEFAULT,
        'MARKDOWN_SUPPORT'        : S_DEFAULT,
        'TOC_INCLUDE_HEADINGS'    : S_DEFAULT,
        'AUTOLINK_SUPPORT'        : S_DEFAULT,
        'BUILTIN_STL_SUPPORT'     : S_DEFAULT,
        'CPP_CLI_SUPPORT'         : S_DEFAULT,
        'SIP_SUPPORT'             : S_DEFAULT,
        'IDL_PROPERTY_SUPPORT'    : S_DEFAULT,
        'DISTRIBUTE_GROUP_DOC'    : S_DEFAULT,
        'GROUP_NESTED_COMPOUNDS'  : S_DEFAULT,
        'SUBGROUPING'             : S_DEFAULT,
        'INLINE_GROUPED_CLASSES'  : S_DEFAULT,
        'INLINE_SIMPLE_STRUCTS'   : S_DEFAULT,
        'TYPEDEF_HIDES_STRUCT'    : S_DEFAULT,
        'LOOKUP_CACHE_SIZE'       : S_DEFAULT,
        'NUM_PROC_THREADS'        : S_DEFAULT,
        'EXTRACT_ALL'             : YES,
        'EXTRACT_PRIVATE'         : S_DEFAULT,
        'EXTRACT_PRIV_VIRTUAL'    : S_DEFAULT,
        'EXTRACT_PACKAGE'         : S_DEFAULT,
        'EXTRACT_STATIC'          : S_DEFAULT,
        'EXTRACT_LOCAL_CLASSES'   : S_DEFAULT,
        'EXTRACT_LOCAL_METHODS'   : S_DEFAULT,
        'EXTRACT_ANON_NSPACES'    : S_DEFAULT,
        'RESOLVE_UNNAMED_PARAMS'  : S_DEFAULT,
        'HIDE_UNDOC_MEMBERS'      : S_DEFAULT,
        'HIDE_UNDOC_CLASSES'      : S_DEFAULT,
        'HIDE_FRIEND_COMPOUNDS'   : S_DEFAULT,
        'HIDE_IN_BODY_DOCS'       : S_DEFAULT,
        'INTERNAL_DOCS'           : YES, # documentation after internal command is included
        'CASE_SENSE_NAMES'        : S_DEFAULT,
        'HIDE_SCOPE_NAMES'        : YES, # full class and namespace scopes in the documentation
        'HIDE_COMPOUND_REFERENCE' : S_DEFAULT,
        'SHOW_HEADERFILE'         : S_DEFAULT,
        'SHOW_INCLUDE_FILES'      : S_DEFAULT,
        'SHOW_GROUPED_MEMB_INC'   : S_DEFAULT,
        'FORCE_LOCAL_INCLUDES'    : S_DEFAULT,
        'INLINE_INFO'             : S_DEFAULT,
        'SORT_MEMBER_DOCS'        : S_DEFAULT,
        'SORT_BRIEF_DOCS'         : YES, # sort the brief descriptions of file namespace and class members alphabetically by member name
        'SORT_MEMBERS_CTORS_1ST'  : S_DEFAULT,
        'SORT_GROUP_NAMES'        : S_DEFAULT,
        'SORT_BY_SCOPE_NAME'      : YES,
        'STRICT_PROTO_MATCHING'   : S_DEFAULT,
        'GENERATE_TODOLIST'       : S_DEFAULT,
        'GENERATE_TESTLIST'       : S_DEFAULT,
        'GENERATE_BUGLIST'        : S_DEFAULT,
        'GENERATE_DEPRECATEDLIST' : S_DEFAULT,
        'ENABLED_SECTIONS'        : S_DEFAULT,
        'MAX_INITIALIZER_LINES'   : S_DEFAULT,
        'SHOW_USED_FILES'         : S_DEFAULT,
        'SHOW_FILES'              : S_DEFAULT,
        'SHOW_NAMESPACES'         : S_DEFAULT,
        'FILE_VERSION_FILTER'     : S_DEFAULT,
        'LAYOUT_FILE'             : S_DEFAULT,
        'CITE_BIB_FILES'          : S_DEFAULT,
        'QUIET'                   : S_DEFAULT,
        'WARNINGS'                : S_DEFAULT,
        'WARN_IF_UNDOCUMENTED'    : S_DEFAULT,
        'WARN_IF_DOC_ERROR'       : S_DEFAULT,
        'WARN_IF_INCOMPLETE_DOC'  : S_DEFAULT,
        'WARN_NO_PARAMDOC'        : YES,
        'WARN_AS_ERROR'           : WARNING_FAIL,
        'WARN_FORMAT'             : S_DEFAULT,
        'WARN_LOGFILE'            : S_AUTO,
        'INPUT'                   : ["."],
        'INPUT_ENCODING'          : S_DEFAULT,
        'FILE_PATTERNS'           : L_DEFAULT_FILE_PATTERN,
        'RECURSIVE'               : YES,
        'EXCLUDE'                 : S_DEFAULT,
        'EXCLUDE_SYMLINKS'        : S_DEFAULT,
        'EXCLUDE_PATTERNS'        : S_AUTO,
        'EXCLUDE_SYMBOLS'         : S_DEFAULT,
        'EXAMPLE_PATH'            : S_DEFAULT,
        'EXAMPLE_PATTERNS'        : S_DEFAULT,
        'EXAMPLE_RECURSIVE'       : S_DEFAULT,
        'IMAGE_PATH'              : S_DEFAULT,
        'INPUT_FILTER'            : S_DEFAULT,
        'FILTER_PATTERNS'         : S_DEFAULT,
        'FILTER_SOURCE_FILES'     : S_DEFAULT,
        'FILTER_SOURCE_PATTERNS'  : S_DEFAULT,
        'USE_MDFILE_AS_MAINPAGE'  : "README.md",
        'SOURCE_BROWSER'          : YES,
        'INLINE_SOURCES'          : YES,
        'STRIP_CODE_COMMENTS'     : S_DEFAULT,
        'REFERENCED_BY_RELATION'  : S_DEFAULT,
        'REFERENCES_RELATION'     : S_DEFAULT,
        'REFERENCES_LINK_SOURCE'  : S_DEFAULT,
        'SOURCE_TOOLTIPS'         : S_DEFAULT,
        'USE_HTAGS'               : S_DEFAULT,
        'VERBATIM_HEADERS'        : S_DEFAULT,
        'CLANG_ASSISTED_PARSING'  : S_DEFAULT,
        'CLANG_ADD_INC_PATHS'     : S_DEFAULT,
        'CLANG_OPTIONS'           : S_DEFAULT,
        'CLANG_DATABASE_PATH'     : S_DEFAULT,
        'ALPHABETICAL_INDEX'      : S_DEFAULT,
        'IGNORE_PREFIX'           : S_DEFAULT,
        'GENERATE_HTML'           : S_DEFAULT,
        'HTML_OUTPUT'             : S_DEFAULT,
        'HTML_FILE_EXTENSION'     : S_DEFAULT,
        'HTML_HEADER'             : S_AUTO, # required for Doxygen Awesome
        'HTML_FOOTER'             : S_DEFAULT,
        'HTML_STYLESHEET'         : S_DEFAULT,
        'HTML_EXTRA_STYLESHEET'   : S_AUTO, # required for Doxygen Awesome
        'HTML_EXTRA_FILES'        : S_AUTO, # required for Doxygen Awesome
        'HTML_COLORSTYLE'         : "LIGHT", # required with Doxygen >= 1.9.5
        'HTML_COLORSTYLE_HUE'     : 209, # required for Doxygen Awesome
        'HTML_COLORSTYLE_SAT'     : 255, # required for Doxygen Awesome
        'HTML_COLORSTYLE_GAMMA'   : 113, # required for Doxygen Awesome
        'HTML_TIMESTAMP'          : YES,
        'HTML_DYNAMIC_MENUS'      : S_DEFAULT,
        'HTML_DYNAMIC_SECTIONS'   : YES,
        'HTML_INDEX_NUM_ENTRIES'  : S_DEFAULT,
        'GENERATE_DOCSET'         : S_DEFAULT,
        'DOCSET_FEEDNAME'         : S_DEFAULT,
        'DOCSET_BUNDLE_ID'        : S_DEFAULT,
        'DOCSET_PUBLISHER_ID'     : S_DEFAULT,
        'DOCSET_PUBLISHER_NAME'   : S_PUBLISHER,
        'GENERATE_HTMLHELP'       : S_DEFAULT,
        'CHM_FILE'                : S_DEFAULT,
        'HHC_LOCATION'            : S_DEFAULT,
        'GENERATE_CHI'            : S_DEFAULT,
        'CHM_INDEX_ENCODING'      : S_DEFAULT,
        'BINARY_TOC'              : S_DEFAULT,
        'TOC_EXPAND'              : S_DEFAULT,
        'GENERATE_QHP'            : S_DEFAULT,
        'QCH_FILE'                : S_DEFAULT,
        'QHP_NAMESPACE'           : S_DEFAULT,
        'QHP_VIRTUAL_FOLDER'      : S_DEFAULT,
        'QHP_CUST_FILTER_NAME'    : S_DEFAULT,
        'QHP_CUST_FILTER_ATTRS'   : S_DEFAULT,
        'QHP_SECT_FILTER_ATTRS'   : S_DEFAULT,
        'QHG_LOCATION'            : S_DEFAULT,
        'GENERATE_ECLIPSEHELP'    : S_DEFAULT,
        'ECLIPSE_DOC_ID'          : S_DEFAULT,
        'DISABLE_INDEX'           : NO, # required for Doxygen Awesome
        'GENERATE_TREEVIEW'       : YES, # required for Doxygen Awesome
        'FULL_SIDEBAR'            : NO, # required for Doxygen Awesome
        'ENUM_VALUES_PER_LINE'    : S_DEFAULT,
        'TREEVIEW_WIDTH'          : S_DEFAULT,
        'EXT_LINKS_IN_WINDOW'     : S_DEFAULT,
        'HTML_FORMULA_FORMAT'     : S_DEFAULT,
        'FORMULA_FONTSIZE'        : S_DEFAULT,
        'FORMULA_TRANSPARENT'     : S_DEFAULT,
        'FORMULA_MACROFILE'       : S_DEFAULT,
        'USE_MATHJAX'             : S_DEFAULT,
        'MATHJAX_VERSION'         : S_DEFAULT,
        'MATHJAX_FORMAT'          : S_DEFAULT,
        'MATHJAX_RELPATH'         : "https://cdn.jsdelivr.net/npm/mathjax@2",
        'MATHJAX_EXTENSIONS'      : S_DEFAULT,
        'MATHJAX_CODEFILE'        : S_DEFAULT,
        'SEARCHENGINE'            : YES,
        'SERVER_BASED_SEARCH'     : NO,
        'EXTERNAL_SEARCH'         : NO,
        'SEARCHENGINE_URL'        : S_DEFAULT,
        'SEARCHDATA_FILE'         : S_DEFAULT,
        'EXTERNAL_SEARCH_ID'      : S_DEFAULT,
        'EXTRA_SEARCH_MAPPINGS'   : S_DEFAULT,
        'GENERATE_LATEX'          : NO,
        'LATEX_OUTPUT'            : S_DEFAULT,
        'LATEX_CMD_NAME'          : "latex",
        'MAKEINDEX_CMD_NAME'      : S_DEFAULT,
        'LATEX_MAKEINDEX_CMD'     : S_DEFAULT,
        'COMPACT_LATEX'           : S_DEFAULT,
        'PAPER_TYPE'              : S_DEFAULT,
        'EXTRA_PACKAGES'          : S_DEFAULT,
        'LATEX_HEADER'            : S_DEFAULT,
        'LATEX_FOOTER'            : S_DEFAULT,
        'LATEX_EXTRA_STYLESHEET'  : S_DEFAULT,
        'LATEX_EXTRA_FILES'       : S_DEFAULT,
        'PDF_HYPERLINKS'          : S_DEFAULT,
        'USE_PDFLATEX'            : S_DEFAULT,
        'LATEX_BATCHMODE'         : S_DEFAULT,
        'LATEX_HIDE_INDICES'      : S_DEFAULT,
        'LATEX_BIB_STYLE'         : S_DEFAULT,
        'LATEX_TIMESTAMP'         : S_DEFAULT,
        'LATEX_EMOJI_DIRECTORY'   : S_DEFAULT,
        'GENERATE_RTF'            : S_DEFAULT,
        'RTF_OUTPUT'              : S_DEFAULT,
        'COMPACT_RTF'             : S_DEFAULT,
        'RTF_HYPERLINKS'          : S_DEFAULT,
        'RTF_STYLESHEET_FILE'     : S_DEFAULT,
        'RTF_EXTENSIONS_FILE'     : S_DEFAULT,
        'GENERATE_MAN'            : S_DEFAULT,
        'MAN_OUTPUT'              : S_DEFAULT,
        'MAN_EXTENSION'           : S_DEFAULT,
        'MAN_SUBDIR'              : S_DEFAULT,
        'MAN_LINKS'               : S_DEFAULT,
        'GENERATE_XML'            : S_DEFAULT,
        'XML_OUTPUT'              : S_DEFAULT,
        'XML_PROGRAMLISTING'      : S_DEFAULT,
        'XML_NS_MEMB_FILE_SCOPE'  : S_DEFAULT,
        'GENERATE_DOCBOOK'        : S_DEFAULT,
        'DOCBOOK_OUTPUT'          : S_DEFAULT,
        'GENERATE_AUTOGEN_DEF'    : S_DEFAULT,
        'GENERATE_PERLMOD'        : S_DEFAULT,
        'PERLMOD_LATEX'           : S_DEFAULT,
        'PERLMOD_PRETTY'          : S_DEFAULT,
        'PERLMOD_MAKEVAR_PREFIX'  : S_DEFAULT,
        'ENABLE_PREPROCESSING'    : S_DEFAULT,
        'MACRO_EXPANSION'         : S_DEFAULT,
        'EXPAND_ONLY_PREDEF'      : S_DEFAULT,
        'SEARCH_INCLUDES'         : S_DEFAULT,
        'INCLUDE_PATH'            : S_DEFAULT,
        'INCLUDE_FILE_PATTERNS'   : S_DEFAULT,
        'PREDEFINED'              : S_DEFAULT,
        'EXPAND_AS_DEFINED'       : S_DEFAULT,
        'SKIP_FUNCTION_MACROS'    : S_DEFAULT,
        'TAGFILES'                : S_DEFAULT,
        'GENERATE_TAGFILE'        : S_DEFAULT,
        'ALLEXTERNALS'            : S_DEFAULT,
        'EXTERNAL_GROUPS'         : S_DEFAULT,
        'EXTERNAL_PAGES'          : S_DEFAULT,
        'CLASS_DIAGRAMS'          : S_DEFAULT,
        'DIA_PATH'                : S_DEFAULT,
        'HIDE_UNDOC_RELATIONS'    : S_DEFAULT,
        'HAVE_DOT'                : YES,
        'DOT_NUM_THREADS'         : S_DEFAULT,
        'DOT_FONTNAME'            : S_DEFAULT,
        'DOT_FONTSIZE'            : S_DEFAULT,
        'DOT_FONTPATH'            : S_DEFAULT,
        'CLASS_GRAPH'             : S_DEFAULT,
        'COLLABORATION_GRAPH'     : S_DEFAULT,
        'GROUP_GRAPHS'            : S_DEFAULT,
        'UML_LOOK'                : YES,
        'UML_LIMIT_NUM_FIELDS'    : S_DEFAULT,
        'DOT_UML_DETAILS'         : S_DEFAULT,
        'DOT_WRAP_THRESHOLD'      : S_DEFAULT,
        'TEMPLATE_RELATIONS'      : S_DEFAULT,
        'INCLUDE_GRAPH'           : S_DEFAULT,
        'INCLUDED_BY_GRAPH'       : S_DEFAULT,
        'CALL_GRAPH'              : S_DEFAULT,
        'CALLER_GRAPH'            : S_DEFAULT,
        'GRAPHICAL_HIERARCHY'     : S_DEFAULT,
        'DIRECTORY_GRAPH'         : S_DEFAULT,
        'DOT_IMAGE_FORMAT'        : "svg",
        'INTERACTIVE_SVG'         : YES,
        'DOT_PATH'                : S_DEFAULT,
        'DOTFILE_DIRS'            : S_DEFAULT,
        'MSCFILE_DIRS'            : S_DEFAULT,
        'DIAFILE_DIRS'            : S_DEFAULT,
        'PLANTUML_JAR_PATH'       : S_PLANTUML_PATH,
        'PLANTUML_CFG_FILE'       : S_DEFAULT,
        'PLANTUML_INCLUDE_PATH'   : S_PLANTUML_PATH,
        'DOT_GRAPH_MAX_NODES'     : S_DEFAULT,
        'MAX_DOT_GRAPH_DEPTH'     : S_DEFAULT,
        'DOT_TRANSPARENT'         : YES,
        'DOT_MULTI_TARGETS'       : YES,
        'GENERATE_LEGEND'         : S_DEFAULT,
        'DOT_CLEANUP'             : YES,
    }
    def __init__(self, s_webside: str = None, s_logo: str = None):
        self.s_webside = s_webside
        self.s_logo = s_logo
        self.l_warnings = []
        self.s_output_dir = ""
        self.s_doxyfile_name = ""
        self.s_warning_name = ""

    def create_default_doxyfile(self, s_file_name: str):
        """!
        @brief Create default doxyfile
        @param  s_file_name : doxygen file name
        """
        subprocess.call([S_DOXYGEN_PATH, "-g", s_file_name])

    def set_configuration(self, s_type: str, value: Any, b_override: bool = True):
        """!
        @brief  Set doxygen configuration.
        @param  s_type : type to set in configuration
        @param  value : value to set for s_type in configuration
        @param  b_override : info if selected default setting should override
        """
        if b_override or (self.get_configuration(s_type) in L_OVERRIDE):
            if s_type in self.d_settings:
                if isinstance(value, list):
                    if self.d_settings[s_type] in L_OVERRIDE:
                        self.d_settings[s_type] = []
                    self.d_settings[s_type].extend(value)
                else:
                    self.d_settings[s_type] = value
            else:
                self.l_warnings.append(f"{s_type} not in configuration to set")

    def get_configuration(self, s_type: str):
        """!
        @brief  Get type in doxygen configuration.
        @param  s_type : type in configuration get setting
        @return configuration settings
        """
        if s_type in self.d_settings:
            value = self.d_settings[s_type]
        else:
            value = "Invalid"
            self.l_warnings.append(f"{s_type} not in configuration to get")
        return value

    def prepare_doxyfile_configuration(self):
        """!
        @brief  Prepare doxfile configuration with default settings that depend on other parameters.
                Parameters that set before as fix parameter or by user will not override.
                This allows the user to make settings that differ from the default configuration.
        """
        # save filenames and directory witch need so save/open files
        self.s_output_dir = f"{self.get_configuration('OUTPUT_DIRECTORY')}/" # save output directory witch used for other file names
        s_project_name = self.get_configuration('PROJECT_NAME')
        self.s_doxyfile_name = f"{self.s_output_dir}{s_project_name}.Doxyfile"
        self.s_warning_name = f"{self.s_output_dir}{S_WARNING_FILE_PREFIX}{s_project_name}{S_WARNING_FILE_SUFFIX}"

        # set uniform doxygen configuration with depend on other parameters
        self.set_configuration('PROJECT_BRIEF', f"{s_project_name}-Documentation", b_override=False) # use project name as default if nothing defined
        self.set_configuration('WARN_LOGFILE', self.s_warning_name, b_override=False)
        self.set_configuration('EXCLUDE_PATTERNS', [self.s_output_dir], b_override=False)

        # write version prefix for version numbers as project number
        s_version = self.get_configuration('PROJECT_NUMBER')
        if s_version not in L_OVERRIDE:
            b_is_version = True
            for s_char in s_version:
                if not (s_char.isdigit or (s_char == ".")):
                    b_is_version = False
                    break
            if b_is_version:
                self.set_configuration('PROJECT_NUMBER', f"v{s_version}")

        # set doxygen awesome settings witch depends on path
        l_extra_files = ["doxygen-awesome-darkmode-toggle.js",
                         "doxygen-awesome-fragment-copy-button.js",
                         "doxygen-awesome-paragraph-link.js",
                         "doxygen-awesome-interactive-toc.js",
                         "doxygen-awesome-tabs.js"]
        self.set_configuration('HTML_EXTRA_FILES', l_extra_files, b_override=False)
        l_extra_stylesheet = ["doxygen-awesome.css",
                              "doxygen-awesome-sidebar-only.css",
                              "doxygen-awesome-sidebar-only-darkmode-toggle.css"]
        self.set_configuration('HTML_EXTRA_STYLESHEET', l_extra_stylesheet, b_override=False) # doxygen styling code
        self.set_configuration('HTML_HEADER', "header.html", b_override=False) # use own doxygen header

    def edit_select_doxyfile_settings(self):
        """!
        @brief  Override default settings in doxyfile with selected settings.
        """
        # load the default doxygen template file
        config_parser = ConfigParser()
        configuration = config_parser.load_configuration(self.s_doxyfile_name)

        # write doxygen settings
        for key, value in self.d_settings.items():
            if value not in L_OVERRIDE:
                if isinstance(value, list):
                    configuration[key] = []
                    for entry in value:
                        configuration[key].append(entry)
                else:
                    if isinstance(value, int):
                        value = str(value) # integer can only write as string to doxyfile
                    configuration[key] = value
            elif value == S_AUTO:
                self.l_warnings.append(f"Setting not written: {key}: {value}") # warn if setting that should override is not set

        # store the configuration in doxyfile
        config_parser.store_configuration(configuration, self.s_doxyfile_name)

    def add_warnings(self):
        """!
        @brief  Add warnings to warning file
        """
        if self.l_warnings:
            with open(self.s_warning_name, mode='a', encoding='utf-8') as file:
                for s_warning in self.l_warnings:
                    file.write(s_warning + "\n")

    def download_plantuml_jar(self):
        """!
        @brief Download PlantUML Jar
        """
        if not os.path.exists(S_PLANTUML_JAR_NAME):
            print(f"Download {S_PLANTUML_JAR_NAME} ...")
            try:
                with requests.get(S_PLANTUML_JAR_URL, timeout=I_TIMEOUT) as response:
                    response.raise_for_status()
                    with open(S_PLANTUML_JAR_NAME, mode='wb') as file: # download plantuml.jar
                        file.write(response.content) # download plantuml.jar
            except requests.Timeout:
                print(f"Timeout for download {S_PLANTUML_JAR_NAME}!")
            except requests.RequestException as e:
                print(f"Can not download {S_PLANTUML_JAR_NAME}! {e}")
        else:
            print(f"{S_PLANTUML_JAR_NAME} already exist!")

    def download_doxygen(self):
        """!
        @brief Download Doxygen
        """
        if not os.path.exists(S_DOXYGEN_PATH) or not os.path.exists(S_DOXYGEN_DLL):
            if not os.path.exists(S_DOXYGEN_ZIP):
                print(f"Download {S_DOXYGEN_ZIP} ...")
                try:
                    with requests.get(S_DOXYGEN_URL, timeout=I_TIMEOUT) as response:
                        response.raise_for_status()
                        with open(S_DOXYGEN_ZIP, mode='wb') as file: # download doxygen
                            file.write(response.content)
                except requests.Timeout:
                    print(f"Timeout for download {S_DOXYGEN_ZIP}!")
                except requests.RequestException as e:
                    print(f"Can not download {S_DOXYGEN_ZIP}! {e}")
            else:
                print(f"{S_DOXYGEN_ZIP} already exist!")
            with zipfile.ZipFile(S_DOXYGEN_ZIP, mode='r') as zip_ref:
                zip_ref.extract(S_DOXYGEN_PATH, S_PLANTUML_PATH)
                zip_ref.extract(S_DOXYGEN_DLL, S_PLANTUML_PATH)
        else:
            print(f"{S_DOXYGEN_PATH} and {S_DOXYGEN_DLL} already exist!")

    def check_doxygen_warnings(self, b_open_warning_file: bool = True) -> bool:
        """!
        @brief  Check for doxygen Warnings
        @param  b_open_warning_file : [True] open warning file; [False] only check for warnings
        @return status if doxygen warnings exist
        """
        b_warnings = False

        if os.path.exists(self.s_warning_name):
            with open(self.s_warning_name, mode='r', encoding='utf-8') as file:
                lines = file.readlines()
                if len(lines) != 0:
                    b_warnings = True
                    print("Doxygen Warnings found!!!")
                    for s_line in lines:
                        print(f"  {s_line}")

        if b_open_warning_file and b_warnings:
            OpenNotepad(self.s_warning_name)

        return b_warnings

    def generate_doxygen_output(self, b_open_doxygen_output: bool = True):
        """!
        @brief Generate Doxygen output depend on existing doxyfile
        @param b_open_doxygen_output : [True] open output in browser; [False] only generate output
        """
        subprocess.call([S_DOXYGEN_PATH, self.s_doxyfile_name])

        if b_open_doxygen_output:
            # open doxygen output
            filename = f"file:///{os.getcwd()}/{self.s_output_dir}{S_INDEX_FILE}"
            webbrowser.open_new_tab(filename)

    def add_github_corner(self):
        """!
        @brief Add Github corner and tab icon
        """
        if self.s_webside is not None:
            s_corner_text = S_GITHUB_CORNER_FIRST + self.s_webside + S_GITHUB_CORNER_LAST
        else:
            s_corner_text = None
        if (self.d_settings['PROJECT_LOGO'] != "") or (self.s_logo is not None):
            if self.s_logo is not None:
                s_icon_file = self.s_logo
            else:
                s_icon_file = self.d_settings['PROJECT_LOGO']
            if '/' in s_icon_file:
                i_index = s_icon_file.rfind('/')
                s_icon_file = s_icon_file[i_index + 1:]
            s_icon_text = f'{S_ICON_FIRST}"{s_icon_file}"{S_ICON_LAST}'
        else:
            s_icon_text = None
        s_folder = f"{self.s_output_dir}html/"
        for file in os.listdir(s_folder):
            if file.endswith(".html"):
                with open(f"{s_folder}{file}", mode='a', encoding='utf-8') as file:
                    if s_corner_text is not None:
                        file.write(s_corner_text + "\n")
                    if s_icon_text is not None:
                        file.write(s_icon_text + "\n")

    def add_images(self):
        """!
        @brief Add images to html folder
        """
        source_folder = f"{self.s_output_dir}/../../img"
        destination_folder = f"{self.s_output_dir}html"
        for filename in os.listdir(source_folder):
            source_path = os.path.join(source_folder, filename)
            destination_path = os.path.join(destination_folder, filename)
            if os.path.isfile(source_path):
                shutil.copy2(source_path, destination_path)
        if self.s_logo is not None:
            shutil.copy2(self.s_logo, os.path.join(destination_folder, os.path.basename(self.s_logo)))

    def add_nojekyll_file(self):
        """!
        @brief Add .nojekyll file that files with underscores visible
        """
        s_file_name = ".nojekyll"
        with open(f"{self.s_output_dir}html/{s_file_name}", mode='w', encoding='utf-8') as file:
            file.write('')

    def generate_configuration_diff(self):
        """!
        @brief  Generate doxyfile diff to view changes
        """
        s_default_doxyfile = f"{self.s_output_dir}/Default.Doxyfile"

        # create and read default doxyfile
        self.create_default_doxyfile(s_default_doxyfile)
        config_parser = ConfigParser()
        configuration = config_parser.load_configuration(s_default_doxyfile)
        config_parser.store_configuration(configuration, s_default_doxyfile)
        with open(s_default_doxyfile, mode='r', encoding='utf-8') as file:
            s_default_config = file.read()
        os.remove(s_default_doxyfile)

        # read modified doxyfile
        with open(self.s_doxyfile_name, mode='r', encoding='utf-8') as file:
            s_modified_config = file.read()

        s_diff_file_name = f'{self.s_output_dir}DoxyfileDiff.html'
        difference = difflib.HtmlDiff(wrapcolumn=I_WRAP_LENGHT).make_file(s_default_config.splitlines(), s_modified_config.splitlines(), "Default", "Modified")
        with open(s_diff_file_name, mode='w', encoding='utf-8') as file:
            file.write(difference)

    def run_doxygen(self, b_open_doxygen_output: bool = True) -> bool:
        """!
        @brief  Generate Doxyfile and Doxygen output depend on doxyfile settings
        @param  b_open_doxygen_output : [True] open output in browser; [False] only generate output
        @return status for found doxygen warning
        """
        self.download_doxygen()
        self.download_plantuml_jar()
        self.prepare_doxyfile_configuration()
        if not os.path.exists(self.s_output_dir):
            os.makedirs(self.s_output_dir)
        self.create_default_doxyfile(self.s_doxyfile_name)
        self.edit_select_doxyfile_settings()
        self.generate_doxygen_output(b_open_doxygen_output)
        self.add_github_corner()
        self.add_images()
        self.add_nojekyll_file()
        self.generate_configuration_diff()

        # additional script to check for valid doxygen specification in python files
        if S_PYTHON_PATTERN in self.d_settings['FILE_PATTERNS']:
            doxy_checker = DoxyPyChecker(S_MAIN_FOLDER_FOLDER)
            l_finding = doxy_checker.run_check()
            self.l_warnings.extend(l_finding)

        self.add_warnings() # add own warnings to warning file
        b_warnings = self.check_doxygen_warnings(b_open_doxygen_output)

        return b_warnings

def get_cmd_args() -> argparse.Namespace:
    """!
    @brief  Function to define CMD arguments.
    @return Function returns argument parser.
    """
    o_parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    o_parser.add_argument("-o", "--open",
                          type = bool,
                          default = False,
                          help = "open output files after generation")
    return o_parser.parse_args()

if __name__ == "__main__":
    args = get_cmd_args()
    doxygen_creator = DoxygenCreator(S_REPO_LINK, f"{S_MAIN_FOLDER_FOLDER}{mdata.S_ICON_32_RESOURCE_PATH}")
    doxygen_creator.set_configuration('PROJECT_NAME', version.__title__)
    doxygen_creator.set_configuration('PROJECT_NUMBER', version.__version__)
    doxygen_creator.set_configuration('PROJECT_BRIEF', version.__description__)
    doxygen_creator.set_configuration('PROJECT_LOGO', f"{S_MAIN_FOLDER_FOLDER}{mdata.S_ICON_RESOURCE_PATH}")
    doxygen_creator.set_configuration('INPUT', S_MAIN_FOLDER_FOLDER)
    l_file_pattern = [S_PYTHON_PATTERN, "*.md"]
    #l_exclude_pattern = ["DoxygenCreator", "Installation", "Executable", "Test", "Documentation", "CONTRIBUTING.md"]
    #doxygen_creator.set_configuration('EXCLUDE_PATTERNS', l_exclude_pattern)
    doxygen_creator.set_configuration('FILE_PATTERNS', l_file_pattern)
    sys.exit(doxygen_creator.run_doxygen(b_open_doxygen_output = args.open))
