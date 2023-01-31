# This Python file uses the following encoding: utf-8
"""!
----------------------------------------------------------------------------------------------------
@file        doxy_py_checker.py
@brief       Check parameter and return value for valid doxygen specification in python files
-----------------------------------------------------------------------------------------------------
"""

import os
import sys
import logging as log
from typing import List
import argparse

S_DEFAULT_PATH = "./"

S_FUNC_DEF = "def "
S_DOC_BRIEF = "@brief "
S_DOC_PARAM = "@param"
S_DOC_RETURN = "@return"
S_FUNC_RETURN = "return"
L_END_COMMENT = ['"""', "'''"]
L_IGNORE_PARAM = ["self"]
S_IGNORE_PARAM_PREFIX = "*"
S_OPTION_RETURN_CODE = "sys.exit"

B_CHECK_TYPING = False

B_DEBUG = False
L_DEBUG_FILE = ["doxy_py_checker.py"]
I_DEBUG_END_LINE = None

def get_leading_spaces(s_string: str) -> int:
    """!
    @brief  get leading spaces of string
    @param s_string : string to check
    @return leading number of spaces
    """
    return len(s_string) - len(s_string.lstrip())

def check_doc_end(s_string : str) -> bool:
    """!
    @brief  Check if string for documentation end
    @param  s_string : string to check
    @return status if string is documentation end
    """
    b_end_found = False
    for s_end_line in L_END_COMMENT:
        if s_end_line in s_string:
            b_end_found = True
            break
    return b_end_found

def check_param_relevant(func_param: str) -> bool:
    """!
    @brief  Check function parameter is relevant to check. "self" and "*" arguments are not relevant.
    @param  func_param : function parameter
    @return status if parameter is relevant
    """
    b_param_relevant = bool((func_param not in L_IGNORE_PARAM) and not func_param.startswith(S_IGNORE_PARAM_PREFIX))
    return b_param_relevant

class ParamCompare:
    """!
    @brief  Compare parameter class
    """
    def __init__(self, l_func_param, l_doc_param):
        self.l_func_param = l_func_param
        self.l_doc_param = l_doc_param
        self.l_report = []

    def check_param_in_doc(self):
        """!
        @brief  Check if all function parameters present in documentation
        """
        for func_param in self.l_func_param:
            if (func_param not in self.l_doc_param) and check_param_relevant(func_param):
                self.l_report.append(f'"{func_param}" is not documented')

    def check_doc_in_param(self):
        """!
        @brief  Check if all documented parameters present in function
        """
        for doc_param in self.l_doc_param:
            b_found = False
            for func_param in self.l_func_param:
                if doc_param == func_param.lstrip(S_IGNORE_PARAM_PREFIX):
                    b_found = True
                    break
            if not b_found:
                self.l_report.append(f'"{doc_param}" is not found in the argument list')

    def compare_param(self) -> List[str]:
        """!
        @brief  Check for valid specification of function parameter
        @return list with findings of parameter compare
        """
        self.check_param_in_doc()
        self.check_doc_in_param()
        return self.l_report

class DoxyPyChecker:
    """!
    @brief  Doxygen documentation checker class
    """
    def __init__(self, path: str = None):
        if path:
            self.s_path = path
        else:
            self.s_path = S_DEFAULT_PATH
        self.l_findings = []

    def get_cmd_args(self) -> argparse.Namespace:
        """!
        @brief  Function to define CMD arguments.
        @return Function returns argument parser.
        """
        o_parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
        o_parser.add_argument("-p", "--path",
                              type = str,
                              help = "set relative path to check for python files")
        return o_parser.parse_args()

    def run_check(self) -> List[str]:
        """!
        @brief  Run doxygen checker
        @return list with findings
        """
        l_files = self.get_file()
        if B_DEBUG:
            l_files = L_DEBUG_FILE
        for file in l_files:
            self.check_file(file)
        i_number_of_warnings = len(self.l_findings)
        print(f"Found {i_number_of_warnings} Warnings in {len(l_files)} files.")
        return self.l_findings

    def get_file(self) -> List[str]:
        """!
        @brief  Get all python files in folder and subfolders
        @return list of all files
        """
        l_files = []
        for root, _dirs, files in os.walk(self.s_path):
            for f in files:
                if os.path.splitext(f)[1] == '.py':
                    fullpath = os.path.join(root, f)
                    l_files.append(fullpath)
        return l_files

    def create_file_link(self, file: str=None, line: int=None, text: str=None) -> str:
        """!
        @brief  Print link to line in file name
        @param  file : file name
        @param  line : line number
        @param  text : optional text behind link
        @return string with file link
        """
        if text is not None:
            s_text = f" {text}"
        else:
            s_text = ""
        s_file_link = f'{file}:{line} {s_text}'
        return s_file_link

    def get_function_parameter(self, s_function_line: str) -> List[str]:
        """!
        @brief  Get Parameter of function
        @param  s_function_line : function line
        @return  list with function parameter
        """
        i_start_pos = s_function_line.find("(")
        i_end_pos = s_function_line.find(")")
        s_param_string = s_function_line[i_start_pos+1:i_end_pos]
        log.debug("Func Param String: %s", s_param_string)
        l_param = []
        i_start = 0
        i_open_bracket = 0
        for i, char in enumerate(s_param_string):
            b_end = (i == (len(s_param_string) - 1))
            if (char == "[") and not b_end:
                i_open_bracket += 1
            elif (char == "]") and not b_end:
                i_open_bracket -= 1
            elif ((char == ",") and (i_open_bracket == 0)) or b_end:
                if b_end:
                    i_end = i + 1
                else:
                    i_end = i
                s_param = s_param_string[i_start:i_end].split(":", maxsplit=1)
                s_param = s_param[0].split("=", maxsplit=1)
                s_param = s_param[0].strip()
                l_param.append(s_param)
                i_start = i + 1
        log.debug("Func Param: %s", l_param)
        return l_param

    def get_doc_param(self, file_content: List[str], i_line_index: int) -> List[str]:
        """!
        @brief  Get specified parameter in doc string.
        @param  file_content : file content
        @param  i_line_index : line index in file content with brief
        @return list with specified parameter
        """
        l_doc_param = []
        for s_line_content in file_content[i_line_index:]:
            l_words = [x.strip() for x in s_line_content.split(maxsplit=2)]
            if l_words:
                if l_words[0] == S_DOC_PARAM:
                    l_doc_param.append(l_words[1].rstrip(":"))
                else:
                    if check_doc_end(s_line_content):
                        break
        log.debug("Doc  Param: %s", l_doc_param)
        return l_doc_param

    def get_func_return_status(self, file_content: List[str], i_line_index: int) -> bool:
        """!
        @brief  Get status if function has return present in documentation.
        @param  file_content : file content
        @param  i_line_index : line index in file content with brief
        @return status if return present in documentation -> True: return found; False: not return; None: return is optional
        """
        b_doc_return_status = False
        b_doc_end = False
        i_func_spaces = get_leading_spaces(file_content[i_line_index])
        for s_line_content in file_content[i_line_index:]:
            s_line = s_line_content[:-1] # delete new line end
            i_line_spaces = get_leading_spaces(s_line)
            if not b_doc_end:
                if check_doc_end(s_line):
                    b_doc_end = True
            else:
                if (i_line_spaces >= i_func_spaces) and s_line.lstrip().startswith(f"{S_FUNC_RETURN} "):
                    b_doc_return_status = True
                    break # return was found in function
                if (i_line_spaces < i_func_spaces) and (len(s_line) > 0) and not s_line.lstrip().startswith("#"): # Indentation deep is lower than function and no empty or comment line
                    break # new function -> no return found
                if (S_OPTION_RETURN_CODE in s_line):
                    b_doc_return_status = None # sys.exit was found -> documentation is optional
        log.debug("Func Return: %s", b_doc_return_status)
        return b_doc_return_status

    def get_doc_return_status(self, file_content: List[str], i_line_index: int) -> bool:
        """!
        @brief  Get status if return present in documentation.
        @param  file_content : file content
        @param  i_line_index : line index in file content with brief
        @return status if return present in documentation
        """
        b_doc_return_status = False
        for s_line_content in file_content[i_line_index:]:
            l_words = [x.strip() for x in s_line_content.split(maxsplit=2)]
            if l_words:
                if l_words[0] == S_DOC_RETURN:
                    b_doc_return_status = True
                    break
                i_end_found = False
                for s_end_line in L_END_COMMENT:
                    if s_end_line in s_line_content:
                        i_end_found = True
                        break
                if i_end_found:
                    break
        log.debug("Doc  Return: %s", b_doc_return_status)
        return b_doc_return_status

    def check_parameter_typing(self, l_parameter: List[str], s_function_line: str) -> list:
        """!
        @brief  Check typing of parameter
        @param  l_parameter : function parameter
        @param  s_function_line : function line
        @return list with function parameter
        """
        l_report = []
        i_start_pos = s_function_line.find("(")
        i_end_pos = s_function_line.find(")")
        s_param_string = s_function_line[i_start_pos+1:i_end_pos]
        for s_param in l_parameter:
            if check_param_relevant(s_param):
                b_typing = False
                i_param_pos = s_param_string.find(s_param)
                for char in s_param_string[i_param_pos:]:
                    if char == ",":
                        break
                    if char == ":":
                        b_typing = True
                if not b_typing:
                    l_report.append(f'parameter "{s_param}" has no typing')
        return l_report

    def check_return_typing(self, b_func_return_status: bool, s_function_line: str) -> List[str]:
        """!
        @brief  Check typing of return
        @param  b_func_return_status : status of  present function return status
        @param  s_function_line : function line
        @return list with function parameter
        """
        l_report = []
        if b_func_return_status:
            i_end_pos = s_function_line.find(")")
            if "->" not in s_function_line[i_end_pos:]:
                l_report.append('return has no typing')
        return l_report

    def check_file(self, s_file_name: str):
        """!
        @brief  Check file for missing parameter description
        @param  s_file_name : file name
        """
        with open(s_file_name, 'r', encoding='utf-8') as file:
            file_content = file.readlines()
        for i, line in enumerate(file_content):
            if S_DOC_BRIEF in line:
                s_function_line = file_content[i-2]
                if s_function_line.lstrip().startswith(S_FUNC_DEF):
                    log.debug("=> Function Line: %s", s_function_line[:-1].lstrip())

                    # check parameter
                    l_func_param = self.get_function_parameter(s_function_line)
                    l_doc_param = self.get_doc_param(file_content, i)
                    param_comp = ParamCompare(l_func_param, l_doc_param)
                    l_report = param_comp.compare_param()

                    # check return
                    b_func_return_status = self.get_func_return_status(file_content, i)
                    if b_func_return_status is not None: # documentation is not optional
                        b_doc_return_status = self.get_doc_return_status(file_content, i)
                        if b_func_return_status != b_doc_return_status:
                            if b_func_return_status:
                                s_report = 'return is not documented'
                            else:
                                s_report = 'return not found in function'
                            l_report.append(s_report)

                    if B_CHECK_TYPING: # check typing
                        l_report.extend(self.check_parameter_typing(l_func_param, s_function_line))
                        l_report.extend(self.check_return_typing(b_func_return_status, s_function_line))

                    # print and save result
                    if l_report:
                        s_file_link = self.create_file_link(s_file_name, i+1)
                        self.l_findings.append(s_file_link)
                        print(s_file_link)
                        for result in l_report:
                            s_report = f"  {result}"
                            self.l_findings.append(s_report)
                            print(s_report)
            if B_DEBUG:
                if I_DEBUG_END_LINE and (i > I_DEBUG_END_LINE):
                    sys.exit("DEBUG_END")

if __name__ == "__main__":
    if B_DEBUG:
        # ----- Debug Logging Configuration -----
        S_LOG_MSG_FORMAT = "%(asctime)s [%(levelname)-5.5s]  %(message)s"
        log.basicConfig(level=log.DEBUG,
                        format=S_LOG_MSG_FORMAT,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[
                            log.FileHandler("doxygen_checker.log"),
                            log.StreamHandler()
                        ])
    doxy_checker = DoxyPyChecker(path="../")
    args = doxy_checker.get_cmd_args()
    if args.path:
        doxy_checker.s_path = args.path
    l_findings = doxy_checker.run_check()
