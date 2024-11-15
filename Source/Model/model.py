"""!
********************************************************************************
@file   model.py
@brief  Application data storage model
********************************************************************************
"""

import logging
from typing import TYPE_CHECKING

from Source.Model import monitor
from Source.version import __title__

if TYPE_CHECKING:
    from Source.Controller.main_window import MainWindow

log = logging.getLogger(__title__)


class Model:
    """!
    @brief Holds the data of the application
    @param ui : main window object
    """

    def __init__(self, ui: "MainWindow"):
        self.ui = ui
        self.c_monitor = monitor.MonitorScale(ui)
