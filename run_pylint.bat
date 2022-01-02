:: "run_pylint.bat"
:: run pylint to analyse python skripts of binokel

set TARGET_FILES=youtube_download.py youtube_api.py youtube_html.py main_window.py
set DISABLE_MSG=
set LOG_FILE=pylint.log

::C0103 invalid constant name (required e.g. snake case)
::C0111 Missing docstring (function, method, module, class, ...)
::C0301 Line too long
::C0325 unnecessary parants (brackets)
::C0326 wrong number of spac (operator, bracket or comma)
::W0511 warning notes (FIXME,XXX,TODO)

pylint %TARGET_FILES% --disable=%DISABLE_MSG% > %LOG_FILE%
notepad %LOG_FILE%

::pause