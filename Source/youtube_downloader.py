# This Python file uses the following encoding: utf-8
"""
*****************************************************************************
 @file    youtube_downloader.py
 @brief   YouTube content downloader
*****************************************************************************
"""

# autopep8: off
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Source.Controller.main_window import YoutubeDownloader # pylint: disable=wrong-import-position
from Source import version # pylint: disable=wrong-import-position
# autopep8: on

if __name__ == "__main__":
    # Set custom application id to show correct icon instead of Python in the task bar
    try:
        from ctypes import windll  # only exists on windows. # pylint: disable=import-outside-toplevel
        app_id = version.__title__ + '.' + version.__version__
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except ImportError:
        pass

    gui = YoutubeDownloader()
    gui.root.mainloop()
