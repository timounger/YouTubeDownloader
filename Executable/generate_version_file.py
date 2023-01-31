# This Python file uses the following encoding: utf-8
"""
*****************************************************************************
 @file    generate_version_file.py
 @brief   YouTubeDownloader - Utility Script to generate a version info .txt file for the executable
*****************************************************************************
"""

import os
import sys

from PyInstaller.utils.win32.versioninfo import *

sys.path.append('../')
import Source.Util.downloader_data as mdata

versionInfo = VSVersionInfo(
    ffi=FixedFileInfo(
        # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
        # Set not needed items to zero 0.
        filevers=(mdata.I_VERSION_MAJOR, mdata.I_VERSION_MINOR, mdata.I_VERSION_PATCH, mdata.I_VERSION_BUILD),
        prodvers=(mdata.I_VERSION_MAJOR, mdata.I_VERSION_MINOR, mdata.I_VERSION_PATCH, mdata.I_VERSION_BUILD),
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
                    u'040904E4',
                    [
                        StringStruct(u'FileDescription', mdata.S_YOUTUBE_DOWNLOADER_DESCRIPTION),
                        StringStruct(u'FileVersion', mdata.S_VERSION),
                        StringStruct(u'LegalCopyright', mdata.S_COPYRIGHT.replace("©", "(c)")),
                        StringStruct(u'ProductName', mdata.S_YOUTUBE_DOWNLOADER_APPLICATION_NAME),
                        StringStruct(u'ProductVersion', mdata.S_VERSION)
                    ])
                ]),
        VarFileInfo([VarStruct(u'Translation', [1033, 1252])])
        ]
    )

if __name__ == "__main__":
    s_workpath = sys.argv[1]
    s_filename = "downloader_version_info.txt"
    s_version_file = os.path.join(s_workpath, s_filename)
    print(f'Generate version file {s_version_file} (Version: {mdata.S_VERSION})')
    os.mkdir(s_workpath) if not os.path.exists(s_workpath) else print(f'Directory {s_workpath} already exists')
    with open(s_version_file, "w") as version_file:
        version_file.write(str(versionInfo))
    sys.exit()
