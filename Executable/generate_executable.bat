:: "generate_executable.bat"
:: generate YouTubeDownloader.exe

@echo off

IF "%~1"=="" (
	echo No explicit python version given. Using folowing:
	python --version
	set path_python_exe=python
) ELSE (
	echo Using python %1
	set path_python_exe=%1
)

set workpath=build

set PYTHONHASHSEED=1

%path_python_exe% .\generate_version_file.py %workpath%
IF %ERRORLEVEL% NEQ 0 (
	exit /b %ERRORLEVEL%
)

%path_python_exe% -m PyInstaller --clean ^
								 --paths ..\..\ ^
								 --add-data ..\Resources\app.ico;Resources ^
								 --icon ..\Resources\app.ico ^
								 --version-file %workpath%\downloader_version_info.txt ^
								 --hidden-import html.parser ^
								 --exclude-module lxml ^
								 --exclude-module typing_extensions ^
								 --exclude-module pygments ^
								 --name YouTubeDownloader ^
								 --onefile ^
								 --noconsole ^
								 --noupx ^
								 --distpath bin ^
								 --workpath %workpath% ^
								 ..\Source\youtube_downloader.py
IF %ERRORLEVEL% NEQ 0 (
	exit /b %ERRORLEVEL%
)

%path_python_exe% .\check_included_packages.py

:: Cleanup
del YouTubeDownloader.spec
::rmdir /s/q "build"
set PYTHONHASHSEED=
pause