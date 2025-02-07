:: "get_package_list.bat"
:: get file with installed packages

@echo off

set ENV_PATH=..\..\.venv
set PY_PATH=%ENV_PATH%\Scripts\python
set PACKAGE_FILE=installed_packages.txt

%PY_PATH% -m pip freeze > %PACKAGE_FILE%

::pause
