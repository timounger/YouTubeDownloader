# This Python file uses the following encoding: utf-8
"""
*****************************************************************************
 @file    youtube_downloader.py
 @brief   YouTube content download
*****************************************************************************
"""

import sys
import ctypes

sys.path.append('../')
import Source.Util.downloader_data as mdata # pylint: disable=wrong-import-position
from Source.Controller.main_window import YoutubeDownloader

if __name__ == "__main__":
    # Set custom application id to show correct icon instead of Python in the task bar
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(mdata.S_APP_ID)
    except ImportError:
        pass

    gui = YoutubeDownloader()
    gui.root.mainloop()
    