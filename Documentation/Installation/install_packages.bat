:: "install_packages.bat"
:: install python packages

:: -r, --requirement <file>    Install from the given requirements file.
:: -c, --constraint <file>     Constrain versions using the given constraints file
:: -U, --upgrade               Upgrade all specified packages to the newest available version
:: --no-cache-dir              Disable the cache.
:: --use-deprecated            Enable deprecated functionality, that will be removed in the future.

@echo off

set ENV_PATH=..\..\.env
set PY_PATH=%ENV_PATH%\Scripts\python

python -m venv %ENV_PATH%
%PY_PATH% -m pip install --upgrade --no-cache-dir --requirement requirements.txt --constraint constraints.txt

::pause
