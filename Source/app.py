"""!
********************************************************************************
@file   app.py
@brief  Application entry file
********************************************************************************
"""

# autopep8: off
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Source.Controller.main_window import MainWindow  # pylint: disable=wrong-import-position
from Source.version import __title__, __version__  # pylint: disable=wrong-import-position
from Source.Util.app_data import S_ICON_REL_PATH  # pylint: disable=wrong-import-position
# autopep8: on


def start_application() -> MainWindow:
    """!
    @brief Start application
    @return windows and application object
    """
    # Set custom application id to show correct icon instead of Python in the task bar
    try:
        from ctypes import windll  # only exists on windows. # pylint: disable=import-outside-toplevel
        app_id = __title__ + "." + __version__
        # log.debug("Setting explicit app user model id: %s", app_id)
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except ImportError:
        pass

    window = MainWindow()

    window.iconbitmap(S_ICON_REL_PATH)

    return window


if __name__ == "__main__":
    o_window = start_application()

    def on_closing():
        o_window.destroy()
    o_window.protocol("WM_DELETE_WINDOW", on_closing)
    o_window.mainloop()
