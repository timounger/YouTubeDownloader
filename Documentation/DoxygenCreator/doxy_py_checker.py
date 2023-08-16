# This Python file uses the following encoding: utf-8
"""!
----------------------------------------------------------------------------------------------------
@file        doxy_py_checker.py
@brief       Check parameter and return value for valid doxygen specification in python files
-----------------------------------------------------------------------------------------------------
"""

import os
from typing import List
import argparse
import ast
import astunparse

S_DEFAULT_PATH = "./"
L_IGNORE_PARAM = ["self", "cls"]
PARAM_DOC_PREFIX = "@param"
RETURN_DOC_PREFIX = "@return"
INIT_FUNCTION = "__init__"

CHECK_TYPING = False

B_DOXY_PY_DEBUG = False
L_DEBUG_FILE = ["doxy_py_checker.py"]

class DoxyPyChecker:
    """!
    @brief  Doxygen documentation checker class
    @param  path : Check python files located in this path
    @param  print_checked_files : status if checked files should print
    """
    def __init__(self, path: str = None, print_checked_files: bool = True):
        self.warnings = []
        if path:
            self.s_path = path
        else:
            self.s_path = S_DEFAULT_PATH
        self.print_checked_files = print_checked_files

    def get_cmd_args(self) -> argparse.Namespace:
        """!
        @brief  Define CMD arguments.
        @return argument parser.
        """
        o_parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
        o_parser.add_argument("-p", "--path",
                              type = str,
                              help = "set relative path to check for python files")
        return o_parser.parse_args()

    def run_check(self) -> List[str]:
        """!
        @brief  Run doxygen checker
        @return list of all files
        """
        findings = []
        l_files = self.get_files()
        if B_DOXY_PY_DEBUG:
            l_files = L_DEBUG_FILE
        for file in l_files:
            if self.print_checked_files:
                print(f"Check docs for file: {file}", )
            findings += self.check_file(file)

            # print result
        if findings:
            print(f"Found {len(findings)} Function with Warnings in {len(l_files)} files.")
            for text in findings:
                print(text)
        else:
            print("All functions correctly documented.")

        return findings

    def get_files(self) -> List[str]:
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

    def check_function(self, func_def: ast.FunctionDef, class_docstring: str = None) -> List[str]:
        """!
        @brief  Check function
        @param  func_def : function definition
        @param  class_docstring : docstring of class
        @return list of findings in function
        """
        findings = []
        documented_params = set()
        docstring = ast.get_docstring(func_def) or class_docstring
        if docstring:
            # Get documented parameters and check for duplicate documentation
            for line in docstring.splitlines():
                if line.lstrip().startswith(PARAM_DOC_PREFIX):
                    param_name = line.split()[1].rstrip(":")
                    if param_name in documented_params:
                        findings.append(f"{param_name} is documented multiple times")
                    else:
                        documented_params.add(param_name)

            # Check that all functional parameters are documented
            for arg in func_def.args.args:
                if arg.arg not in L_IGNORE_PARAM:
                    if arg.arg not in documented_params:
                        findings.append(f"{arg.arg} is not documented")
                    if CHECK_TYPING and arg.annotation is None:
                        findings.append(f"{arg.arg} has no typing")

            # Check that the documented parameters are present
            for documented_param in documented_params:
                all_args = [arg.arg for arg in func_def.args.args]
                if func_def.args.vararg:
                    all_args.append(func_def.args.vararg.arg)
                if func_def.args.kwarg:
                    all_args.append(func_def.args.kwarg.arg)
                if documented_param not in all_args:
                    findings.append(f"{documented_param} is documented but not used")

            # Check that the function return is correctly specified: True: need doc, False no doc, None: optional doc
            doc_has_return = RETURN_DOC_PREFIX in docstring
            func_has_return = False
            for node in ast.walk(func_def):
                if isinstance(node, ast.Return) and node.value is not None: # function has no return None
                    func_has_return = True
                    break
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "exit":
                    module = node.func.value
                    if isinstance(module, ast.Name) and module.id == "sys":
                        func_has_return = None # documentation of "sys.exit" is optional
            if func_has_return is not None:
                if doc_has_return != func_has_return:
                    if func_has_return:
                        findings.append("Return type is not documented")
                    else:
                        findings.append("Return type is documented but not used")
            if CHECK_TYPING and func_has_return:
                return_annotation = astunparse.unparse(func_def.returns).strip() if func_def.returns else None
                if return_annotation is None:
                    findings.append("Return type has no typing")

        return findings

    def check_file(self, file_path: str) -> List[str]:
        """!
        @brief  Check file for missing parameter description
        @param  file_path : file name
        @return list of findings in file
        """
        with open(file_path, mode='r', encoding='utf-8') as file:
            code = file.read()

        tree = ast.parse(code)

        file_findings = []
        for node in ast.walk(tree):
            func_def = None
            check_findings = []
            if isinstance(node, ast.ClassDef):
                class_docstring = ast.get_docstring(node)
                for subnode in node.body:
                    if isinstance(subnode, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if subnode.name == INIT_FUNCTION:
                            func_def = subnode
                            check_findings = self.check_function(func_def, class_docstring)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_def = node
                check_findings = self.check_function(func_def)

            # print findings
            function_finding = ""
            if func_def and check_findings:
                function_finding = f"{file_path}:{func_def.lineno} {func_def.name}"
            for warning in check_findings:
                function_finding += f"\n  {warning}"

            if function_finding:
                file_findings.append(function_finding)

        return file_findings

if __name__ == "__main__":
    doxy_checker = DoxyPyChecker(path="../../", print_checked_files=False)
    args = doxy_checker.get_cmd_args()
    if args.path:
        doxy_checker.s_path = args.path
    doxy_checker.run_check()