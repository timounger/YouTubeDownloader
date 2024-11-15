:: mypy typing checker
:: see https://pypi.org/project/mypy/

@echo off

set MAIN_DIR=..\
set TEST_DIR=Test
set TARGET_DIR=Source
set CONFIG_FILE=%TEST_DIR%\mypy.ini
set LOG_FILE=%TEST_DIR%\mypy.log
set PY_PATH=.env\Scripts\python

cd %MAIN_DIR%

%PY_PATH% -m mypy --config-file=%CONFIG_FILE% %TARGET_DIR% > %LOG_FILE%
echo 'mypy exit code: %ERRORLEVEL%'>>%LOG_FILE%
start notepad %LOG_FILE%
if %ERRORLEVEL% NEQ 0 (
  type %LOG_FILE%
  echo Mypy failed with error code %ERRORLEVEL%.
  exit /b %ERRORLEVEL%
) else (
  type %LOG_FILE%
  echo Mypy check passed.
)

::pause
