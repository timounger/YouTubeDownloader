"""!
*****************************************************************************
@file   mainwindow_tk_ui.py
@brief  Main Window with tkinter
*****************************************************************************
"""

from tkinter import IntVar, StringVar
from customtkinter import CTkLabel, CTkButton, CTkRadioButton, CTkEntry, CTkProgressBar

PADX = 10
PADY = 2

HIGH_RESOLUTION = 1
LOW_RESOLUTION = 2
ONLY_AUDIO = 3

D_FORMAT = {
    HIGH_RESOLUTION: "Hohe Auflösung",
    LOW_RESOLUTION: "Niedrige Auflösung",
    ONLY_AUDIO: "Nur Audio",
}

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.geometry("350x360")

        self.o_url_choice = StringVar()
        self.choice_var = IntVar()

        # Song Title
        self.title_lbl = CTkLabel(self)
        self.title_lbl.grid(columnspan=2, padx=PADX, pady=PADY, sticky="ew")

        # progress bar
        self.progress_bar = CTkProgressBar(self, height=20)
        self.progress_bar.set(0)
        self.progress_bar.grid(columnspan=2, padx=PADX, pady=PADY, sticky="ew")

        # Status Message
        self.status_lbl = CTkLabel(self)
        self.status_lbl.grid(columnspan=2, padx=PADX, pady=PADY, sticky="ew")

        # Entry Box
        self.url_input = CTkEntry(self, textvariable=self.o_url_choice)
        self.url_input.grid(columnspan=2, padx=PADX, pady=PADY, sticky="ew")
        self.insert_btn = CTkButton(self)
        self.insert_btn.grid(row=5, column=0, padx=PADX, pady=PADY, sticky="ew")
        self.direct_btn = CTkButton(self)
        self.direct_btn.grid(row=5, column=1, padx=PADX, pady=PADY, sticky="ew")

        # format label
        self.format_lbl = CTkLabel(self)
        self.format_lbl.grid(columnspan=2, padx=PADX, pady=PADY, sticky="w")
        # format radio button
        for val, txt in D_FORMAT.items():
            format_radio_btn = CTkRadioButton(self, text=txt,
                                              variable=self.choice_var, value=val)
            format_radio_btn.grid(columnspan=2, padx=PADX, pady=PADY, sticky="ew")
        self.choice_var.set(ONLY_AUDIO)  # set first radio button as default
        # download button
        self.download_btn = CTkButton(self)
        self.download_btn.grid(columnspan=2, padx=PADX, pady=PADY, sticky="ew")
        # folder button
        self.open_folder_btn = CTkButton(self, command=self.open_download_folder)
        self.open_folder_btn.grid(columnspan=2, padx=PADX, pady=PADY, sticky="ew")
        # developer Label
        self.copyright_lbl = CTkLabel(self)
        self.copyright_lbl.grid(columnspan=2, padx=PADX, pady=PADY, sticky="ew")
