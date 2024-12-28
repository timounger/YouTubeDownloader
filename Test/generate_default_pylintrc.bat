:: "generate_default_pylintrc.bat"
:: generate default pylintrc file

..\.venv\Scripts\python -m pylint --generate-rcfile > .pylintrc
