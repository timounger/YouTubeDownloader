"""!
********************************************************************************
@file   monitor.py
@brief  handle windows size and scale factor and update items
********************************************************************************
"""

import logging
from typing import Optional, TYPE_CHECKING
import customtkinter
import darkdetect

from Source.version import __title__
from Source.Util.app_data import ETheme

if TYPE_CHECKING:
    from Source.Controller.main_window import MainWindow

log = logging.getLogger(__title__)


class MonitorScale():
    """!
    @brief Class to scale text and item positions.
    @param ui : main window object
    """

    def __init__(self, ui: "MainWindow"):
        self.ui = ui
        self.e_style = ETheme.SYSTEM  # set theme here
        self.e_actual_theme = ETheme.LIGHT
        self.check_for_style_change(self.e_style)

    def check_for_style_change(self, e_style: Optional[ETheme] = None) -> None:
        """!
        @brief Check for style change
        @param e_style : style to set
        """
        if e_style is None:
            e_style = self.e_style
        old_style = self.e_actual_theme
        match e_style:
            case ETheme.LIGHT:
                self.e_actual_theme = ETheme.LIGHT
            case ETheme.DARK:
                self.e_actual_theme = ETheme.DARK
            case ETheme.SYSTEM:
                self.e_actual_theme = ETheme.LIGHT if darkdetect.isLight() else ETheme.DARK
            case _:
                log.warning("Invalid theme change: %s", e_style)
        if old_style != self.e_actual_theme:
            self.set_dialog_style()

    def update_darkmode_status(self, e_style: ETheme) -> None:
        """!
        @brief Update dark mode status.
        @param e_style : select theme mode
        """
        self.e_style = e_style
        self.check_for_style_change(self.e_style)
        self.set_dialog_style()

    def set_dialog_style(self) -> None:
        """!
        @brief Set dialog theme style.
        """
        match self.e_actual_theme:
            case ETheme.LIGHT:
                customtkinter.set_appearance_mode("light")
            case ETheme.DARK:
                customtkinter.set_appearance_mode("dark")
            case _:
                log.warning("Invalid actual theme: %s", self.e_actual_theme)

    def is_light_theme(self) -> bool:
        """!
        @brief get status for active light theme (or classic -> not dark).
        @return status if theme is light
        """
        light_status = bool(self.e_actual_theme != ETheme.DARK)
        return light_status
