:: "generate_default_pylintrc.bat"
:: generate default pylintrc file

..\.env\Scripts\python -m pylint --generate-rcfile > .pylintrc
