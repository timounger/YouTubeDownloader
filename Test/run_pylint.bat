:: "run_pylint.bat"
:: run pylint over YouTubeDownloader code

@echo off

set MAIN_DIR=..\
set TEST_DIR=Test
set TARGET_DIR=Source
set IGNORE_LIST=
set CONFIG_FILE=%TEST_DIR%\.pylintrc
set LOG_FILE=%TEST_DIR%\pylint_YouTubeDownloader.log

cd %MAIN_DIR%
pylint --rcfile=%CONFIG_FILE% %TARGET_DIR% --reports=y --output=%LOG_FILE% --output-format=text --ignore=%IGNORE_LIST%
::type %LOG_FILE%
echo 'pylint exit code: %ERRORLEVEL%'>>%LOG_FILE%
start notepad %LOG_FILE%
if errorlevel 1 (
  echo Pylint failed with error code %errorlevel%.
  exit /b %errorlevel%
) else (
  echo Pylint check passed.
)