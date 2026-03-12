"""!
********************************************************************************
@file   monitor.py
@brief  Theme management for the application window.
********************************************************************************
"""

import logging
from typing import TYPE_CHECKING
import customtkinter
import darkdetect

from Source.version import __title__
from Source.Util.app_data import ETheme

if TYPE_CHECKING:
    from Source.Controller.main_window import MainWindow

log = logging.getLogger(__title__)


class ThemeManager:
    """!
    @brief Manages the application theme (light/dark/system) and applies it to the UI.
    @param ui : main window instance to apply theme changes to
    """

    def __init__(self, ui: "MainWindow"):
        self.ui = ui
        self.selected_theme = ETheme.SYSTEM
        self.active_theme = ETheme.LIGHT
        self.resolve_active_theme(self.selected_theme)

    def resolve_active_theme(self, selected_theme: ETheme | None = None) -> None:
        """!
        @brief Resolve selected theme to a concrete active theme (light or dark).
        @param selected_theme : theme enum to resolve (SYSTEM is mapped to LIGHT/DARK based on OS setting)
        """
        if selected_theme is None:
            selected_theme = self.selected_theme
        previous_theme = self.active_theme
        match selected_theme:
            case ETheme.LIGHT | ETheme.DARK:
                self.active_theme = selected_theme
            case ETheme.SYSTEM:
                self.active_theme = ETheme.LIGHT if darkdetect.isLight() else ETheme.DARK
            case _:
                log.warning("Invalid theme change: %s", selected_theme)
        if previous_theme != self.active_theme:
            self.apply_dialog_theme()

    def apply_theme(self, selected_theme: ETheme) -> None:
        """!
        @brief Set a new theme selection and apply it to the UI.
        @param selected_theme : theme enum to activate
        """
        self.selected_theme = selected_theme
        self.resolve_active_theme(self.selected_theme)
        self.apply_dialog_theme()

    def apply_dialog_theme(self) -> None:
        """!
        @brief Apply the active theme to the customtkinter appearance mode.
        """
        match self.active_theme:
            case ETheme.LIGHT:
                customtkinter.set_appearance_mode("light")
            case ETheme.DARK:
                customtkinter.set_appearance_mode("dark")
            case _:
                log.warning("Invalid actual theme: %s", self.active_theme)

    def is_light_theme(self) -> bool:
        """!
        @brief Check if the active theme is light.
        @return True if active theme is light
        """
        return self.active_theme != ETheme.DARK
