:: Main folder
cd ../../

echo Install Packages
cd ./Documentation/Installation
call install_packages.bat
cd ../../

echo Run Doxygen
cd ./Documentation/DoxygenCreator
..\..\.env\Scripts\python create_doxygen.py
cd ../../

echo Run PyLint
cd ./Test
call run_pylint.bat
::cd ../

echo Build Executable
cd ./Executable
call generate_executable.bat
cd ../

echo Build Setup
cd ./Executable
call generate_setup.bat
cd ../

pause
