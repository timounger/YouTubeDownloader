:: "run_pylint.bat"
:: run pylint over code

@echo off

set MAIN_DIR=..\
set TEST_DIR=Test
set TARGET_DIR=Source
set CONFIG_FILE=%TEST_DIR%\.pylintrc
set LOG_FILE=%TEST_DIR%\pylint.log
set PY_PATH=.venv\Scripts\python

cd %MAIN_DIR%

%PY_PATH% -m pylint --rcfile=%CONFIG_FILE% --reports=y --output-format=text --output=%LOG_FILE% %TARGET_DIR%
echo 'pylint exit code: %ERRORLEVEL%'>>%LOG_FILE%
start notepad %LOG_FILE%
if %ERRORLEVEL% NEQ 0 (
  type %LOG_FILE%
  echo Pylint failed with error code %ERRORLEVEL%.
  exit /b %ERRORLEVEL%
) else (
  type %LOG_FILE%
  echo Pylint check passed.
)
