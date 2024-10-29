"""!
********************************************************************************
@file   monitor.py
@brief  handle windows size and scale factor and update items
********************************************************************************
"""

import sv_ttk
import darkdetect

from Source.Util.app_data import ETheme


class MonitorScale():
    """!
    @brief Class to scale text and item positions.
    @param ui : main window object
    """

    def __init__(self, ui):
        self.ui = ui
        # Theme
        # self.e_style = read_theme_settings()
        self.e_style = ETheme.LIGHT
        self.e_actual_theme = ETheme.LIGHT
        self.check_for_style_change(self.e_style)

    def check_for_style_change(self, e_style: ETheme = None):
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
            case ETheme.CLASSIC:
                self.e_actual_theme = ETheme.CLASSIC
            case ETheme.SYSTEM:
                self.e_actual_theme = ETheme.LIGHT if darkdetect.isLight() else ETheme.DARK
            case _:
                self.ui.set_status(f"Invalid theme change: {e_style}", True)  # state not possible
        if old_style != self.e_actual_theme:
            self.update_icons()
            self.set_dialog_style(self.ui)

    def update_darkmode_status(self, e_style: ETheme):
        """!
        @brief Update dark mode status.
        @param e_style : select theme mode
        """
        self.e_style = e_style
        # write_theme_settings(self.e_style)
        self.check_for_style_change(self.e_style)
        self.set_dialog_style(self.ui)
        # self.set_change_theme_status()
        self.update_icons()
        if hasattr(self.ui, 'status_timer'):  # object does not exist before
            self.ui.update_screen()

    def set_change_theme_status(self):
        """!
        @brief Set dialog theme style.
        """
        match self.e_style:
            case ETheme.LIGHT:
                self.ui.set_status(["Light Theme set", "Heller Modus aktiviert"])
            case ETheme.DARK:
                self.ui.set_status(["Dark Theme set", "Dunkler Modus aktiviert"])
            case ETheme.CLASSIC:
                self.ui.set_status(["Classic Theme set", "Klassischer Modus aktiviert"])
            case ETheme.SYSTEM:
                self.ui.set_status(["System Default Theme set", "System Standard Modus aktiviert"])
            case _:
                self.ui.set_status(f"Invalid theme setting: {self.e_style}", True)  # state not possible

    def set_dialog_style(self, dialog):
        """!
        @brief Set dialog theme style.
        @param dialog : set style to this dialog
        """
        match self.e_actual_theme:
            case ETheme.LIGHT:
                sv_ttk.set_theme("light")
            case ETheme.DARK:
                sv_ttk.set_theme("dark")
            case ETheme.CLASSIC:
                style = ttk.Style()
                style.theme_use(None)  # TODO do not overide all elements back to default
            case _:
                self.ui.set_status(f"Invalid actual theme: {self.e_actual_theme}", True)  # state not possible

    def is_light_theme(self) -> bool:
        """!
        @brief get status for active light theme (or classic -> not dark).
        @return status if theme is light
        """
        light_status = bool(self.e_actual_theme != ETheme.DARK)
        return light_status

    def update_icons(self):
        """!
        @brief Update icons to change between light and dark items depend on theme state.
        """
        b_light_theme = self.is_light_theme()
        """
        config_menu(self.ui.menu_style, icon=ICON_THEME_LIGHT if b_light_theme else ICON_THEME_DARK)
        config_menu(self.ui.menu_log_verbosity, icon=ICON_LOG_LIGHT if b_light_theme else ICON_LOG_DARK)
        config_menu(self.ui.action_help, icon=ICON_HELP_LIGHT if b_light_theme else ICON_HELP_DARK)
        config_menu(self.ui.action_about_app, icon=S_ICON_REL_PATH)
        config_menu(self.ui.action_reset, icon=ICON_RESET_LIGHT if b_light_theme else ICON_RESET_DARK)
        """
