# This Python file uses the following encoding: utf-8
"""
*****************************************************************************
 @file    generate_version_file.py
 @brief   YouTubeDownloader - Utility Script to generate a version info .txt file for the executable
*****************************************************************************
"""

import sys
import os

from PyInstaller.utils.win32.versioninfo import VSVersionInfo, FixedFileInfo, StringFileInfo, StringTable, StringStruct, VarFileInfo, VarStruct

sys.path.append('../')
from Source import version # pylint: disable=wrong-import-position

versionInfo = VSVersionInfo(
    ffi=FixedFileInfo(
        # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
        # Set not needed items to zero 0.
        filevers=(version.VERSION_MAJOR, version.VERSION_MINOR, version.VERSION_PATCH, version.VERSION_BUILD),
        prodvers=(version.VERSION_MAJOR, version.VERSION_MINOR, version.VERSION_PATCH, version.VERSION_BUILD),
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
                    '040904E4',
                    [
                        StringStruct('FileDescription', version.__description__),
                        StringStruct('FileVersion', version.__version__),
                        StringStruct('LegalCopyright', version.__copyright__),
                        StringStruct('ProductName', version.__title__),
                        StringStruct('ProductVersion', version.__version__)
                    ])
                ]),
        VarFileInfo([VarStruct('Translation', [1033, 1252])])
        ]
    )

if __name__ == "__main__":
    s_workpath = sys.argv[1]
    #s_workpath = "build"
    s_filename = "downloader_version_info.txt"
    s_version_file = os.path.join(s_workpath, s_filename)
    print(f'Generate version file {s_version_file} (Version: {version.__version__})')
    if not os.path.exists(s_workpath):
        os.mkdir(s_workpath)
    else:
        print(f'Directory {s_workpath} already exists')
    with open(s_version_file, mode='w', encoding='utf-8') as version_file:
        version_file.write(str(versionInfo))
    sys.exit()
