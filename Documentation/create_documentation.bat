:: create Doxygen documentation

@echo off
cd DoxygenCreator
rmdir /s/q "Output_Doxygen"
..\..\.venv\Scripts\python create_doxygen.py -o True
pause
