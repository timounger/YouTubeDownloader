:: "uninstall_packages.bat"
:: uninstall all packages

@echo off
set package_file=installed_packages.txt
python -m pip freeze > %package_file%
python -m pip uninstall -r %package_file% -y
del %package_file%

pause