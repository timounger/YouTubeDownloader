"""!
*****************************************************************************
@file   dialog_help_ui_tk.py
@brief  Help dialog with tkinter
*****************************************************************************
"""

import tkinter as tk
from tkinter import ttk


class Ui_HelpDialog(object):
    def setupUi(self, HelpDialog):
        HelpDialog.title("Help")
        HelpDialog.geometry("700x400")

        self.tabWidget_helpMenu = ttk.Notebook(HelpDialog)
        self.tabWidget_helpMenu.pack(expand=1, fill="both")

        self.tabHelpGeneral = ttk.Frame(self.tabWidget_helpMenu)
        self.tabWidget_helpMenu.add(self.tabHelpGeneral, text="General")
        self.helpTextGeneral = tk.Text(self.tabHelpGeneral, wrap="word")
        self.helpTextGeneral.pack(fill="both", expand=1)

        self.tab_configuration = ttk.Frame(self.tabWidget_helpMenu)
        self.tabWidget_helpMenu.add(self.tab_configuration, text="Download")
        self.helpTextConfiguration = tk.Text(self.tab_configuration, wrap="word")
        self.helpTextConfiguration.pack(fill="both", expand=1)

    def show(self):
        pass  # TODO
        # self.init_help()
        # self.mainloop()

    def close(self):
        pass  # TODO
        # if self is not None:
        # self.destroy()
