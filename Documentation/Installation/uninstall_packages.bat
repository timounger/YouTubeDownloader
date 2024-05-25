:: "uninstall_packages.bat"
:: uninstall all packages

@echo off

set ENV_PATH=..\..\.env
set PY_PATH=%ENV_PATH%\Scripts\python

set package_file=installed_packages.txt
%PY_PATH% -m pip freeze > %package_file%
%PY_PATH% -m pip uninstall -r %package_file% -y
del %package_file%

pause
