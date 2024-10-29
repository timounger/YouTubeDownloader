"""!
********************************************************************************
@file   model.py
@brief  Application data storage model
********************************************************************************
"""

from Source.Model import monitor


class Model:
    """!
    @brief Holds the data of the application
    @param ui : main window object
    """

    def __init__(self, ui):
        self.ui = ui
        self.c_monitor = monitor.MonitorScale(ui)
