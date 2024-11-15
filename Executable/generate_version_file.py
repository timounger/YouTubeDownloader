"""!
********************************************************************************
@file   generate_version_file.py
@brief  Utility script to create a version info .txt file for the executable.
********************************************************************************
"""

# autopep8: off
import sys
import os
import logging

from PyInstaller.utils.win32.versioninfo import VSVersionInfo, FixedFileInfo, StringFileInfo, StringTable, StringStruct, VarFileInfo, VarStruct

if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Source.version import VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH, VERSION_BUILD, __title__, __description__, __version__, __copyright__ # pylint: disable=wrong-import-position

log = logging.getLogger("GenerateVersionFile")
# autopep8: on

versionInfo = VSVersionInfo(
    ffi=FixedFileInfo(
        # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
        # Set not needed items to zero 0.
        filevers=(VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH, VERSION_BUILD),
        prodvers=(VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH, VERSION_BUILD),
        # Contains a bitmask that specifies the Boolean attributes of the file
        mask=0x0,
        # Contains a bitmask that specifies the Boolean attributes of the file.
        flags=0x0,
        # THe operating system for which this flag was designed
        # 0x4 - NT and there no need to change it.
        OS=0x0,
        # The general type of file.
        # 0x1 - the function is not defined for this fileType
        subtype=0x0,
        # Creation date and time stamp.
        date=(0, 0)
    ),
    kids=[
        StringFileInfo(
            [
                StringTable(
                    "040904E4",
                    [
                        StringStruct("FileDescription", __description__),
                        StringStruct("FileVersion", __version__),
                        StringStruct("LegalCopyright", __copyright__),
                        StringStruct("ProductName", __title__),
                        StringStruct("ProductVersion", __version__)
                    ])
            ]),
        VarFileInfo([VarStruct("Translation", [1033, 1252])])
    ]
)


def generate_version_file(s_filename: str, s_workpath: str) -> None:
    """!
    @brief Generate version file
    @param s_filename : version file name
    @param s_workpath : workpath
    """
    s_version_file = os.path.join(s_workpath, s_filename)
    log.info("Generate version file %s (Version: %s)", s_version_file, __version__)
    if not os.path.exists(s_workpath):
        os.mkdir(s_workpath)
    else:
        log.info("Directory %s already exists", s_workpath)
    with open(s_version_file, mode="w", encoding="utf-8") as version_file:
        version_file.write(str(versionInfo))


if __name__ == "__main__":
    workpath = sys.argv[1]
    filename = "version_info.txt"
    generate_version_file(filename, workpath)
    sys.exit()
