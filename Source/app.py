"""!
********************************************************************************
@file   app.py
@brief  Application entry file
********************************************************************************
"""

# autopep8: off
import sys
import os
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Source.Controller.main_window import MainWindow  # pylint: disable=wrong-import-position
from Source.version import __title__, __version__  # pylint: disable=wrong-import-position
from Source.Util.app_data import ICON_APP  # pylint: disable=wrong-import-position
from Source.Util.colored_log import init_console_logging  # pylint: disable=wrong-import-position
# autopep8: on

log = logging.getLogger(__title__)


def start_application() -> MainWindow:
    """!
    @brief Start application
    @return windows and application object
    """
    # Set custom application id to show correct icon instead of Python in the task bar
    try:
        from ctypes import windll  # only exists on windows. # pylint: disable=import-outside-toplevel
        app_id = __title__ + "." + __version__
        log.debug("Setting explicit app user model id: %s", app_id)
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except ImportError:
        pass

    window = MainWindow()

    window.iconbitmap(ICON_APP)

    return window


if __name__ == "__main__":
    init_console_logging(logging.WARNING)
    o_window = start_application()
    o_window.mainloop()
