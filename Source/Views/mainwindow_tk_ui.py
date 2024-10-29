"""!
*****************************************************************************
@file   mainwindow_tk.py
@brief  Main Window with tkinter
*****************************************************************************
"""

from tkinter import ttk, Button, Text, Menu, IntVar, Label, SUNKEN, W, X, BOTTOM, Entry, StringVar, Radiobutton
from tkinter.ttk import Progressbar, Style

WIDTH = 350
HIGH = 30
DISTANCE = 25

L_FORMAT = [
    ("Hohe Auflösung", 1),
    ("Niedrige Auflösung", 2),
    ("Nur Audio", 3)
]

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.geometry("350x320")

        self.o_url_choice = StringVar()
        self.choice_var = IntVar()
        y = 0

        # YouTube Link Label
        self.url_lbl = Label(self)
        self.url_lbl.place(x=0, y=y, width=WIDTH, height=HIGH)
        y += DISTANCE

        # Entry Box
        self.url_input = Entry(self, width=50, textvariable=self.o_url_choice)
        self.url_input.place(x=0, y=y, width=WIDTH, height=HIGH)
        y += DISTANCE
        self.insert_btn = Button(self, width=10)
        self.insert_btn.place(x=0, y=y, width=WIDTH, height=HIGH)
        y += DISTANCE

        # Error Message
        self.status_lbl = Label(self)
        self.status_lbl.place(x=0, y=y, width=WIDTH, height=HIGH)
        y += DISTANCE

        # Title Message
        self.title_lbl = Label(self, text="Aktueller Song")
        self.title_lbl.place(x=0, y=y, width=WIDTH, height=HIGH)
        y += DISTANCE

        # progress bar
        self.style = Style(self)
        self.style.layout('text.Horizontal.TProgressbar',
                          [('Horizontal.Progressbar.trough',
                            {'children': [('Horizontal.Progressbar.pbar',
                                           {'side': 'left', 'sticky': 'ns'})],
                             'sticky': 'nswe'}),
                              ('Horizontal.Progressbar.label', {'sticky': ''})])
        self.style.configure('text.Horizontal.TProgressbar', text='0 %')
        self.progress_bar = Progressbar(self, style='text.Horizontal.TProgressbar',
                                      length=200, maximum=100, value=0)
        self.progress_bar.place(x=0, y=y, width=WIDTH, height=HIGH)
        y += DISTANCE
        # format label
        self.formal_lbl = Label(self)
        self.formal_lbl.place(x=0, y=y, width=WIDTH, height=HIGH)
        y += DISTANCE
        # format radio button
        for txt, val in L_FORMAT:
            format_radio_btn = Radiobutton(self, text=txt, padx=20,
                                   variable=self.choice_var, value=val)
            format_radio_btn.place(x=0, y=y, width=WIDTH, height=HIGH)
            y += DISTANCE
        self.choice_var.set(1)  # set first radio button as default
        # download button
        self.download_btn = Button(self, width=10)
        self.download_btn.place(x=0, y=y, width=WIDTH, height=HIGH)
        y += DISTANCE
        # folder button
        self.open_folder_btn = Button(self, width=15, command=self.open_download_folder)
        self.open_folder_btn.place(x=0, y=y, width=WIDTH, height=HIGH)
        y += DISTANCE
        # developer Label
        self.copyright_lbl = Label(self)
        self.copyright_lbl.place(x=0, y=y, width=WIDTH, height=HIGH)
        y += DISTANCE

        # Menu (Set icon variable as list (->[None]) to set icon by pointer)
        self.menubar = Menu(self)
        self.config(menu=self.menubar)
        # === Settings ===
        self.menu_settings = (self.menubar, 1, None)
        self.menu_settings_sub = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Einstellungen", menu=self.menu_settings_sub)
        # Sound
        self.action_sound = (self.menu_settings_sub, 0, [None])
        self.menu_settings_sub.add_command(label="Ton")
        # Theme
        self.menu_style = (self.menu_settings_sub, 1, [None])
        self.menu_style_sub = Menu(self.menu_settings_sub, tearoff=0)
        theme_var = IntVar()
        self.action_light = (self.menu_style_sub, 0, None, theme_var)
        self.menu_style_sub.add_radiobutton(label="Hell", variable=theme_var, value=1)
        self.action_dark = (self.menu_style_sub, 1, None, theme_var)
        self.menu_style_sub.add_radiobutton(label="Dunkel", variable=theme_var, value=2)
        self.action_normal = (self.menu_style_sub, 2, None, theme_var)
        self.menu_style_sub.add_radiobutton(label="Classic", variable=theme_var, value=3)
        self.action_system = (self.menu_style_sub, 3, None, theme_var)
        self.menu_style_sub.add_radiobutton(label="System", variable=theme_var, value=4)
        self.menu_settings_sub.add_cascade(label="Thema", menu=self.menu_style_sub)
        # ---
        self.menu_settings_sub.add_separator()
        # Verbosity
        self.menu_log_verbosity = (self.menu_settings_sub, 5, [None])
        self.menu_log_verbosity_sub = Menu(self.menu_settings_sub, tearoff=0)
        log_var = IntVar()
        self.action_log_error = (self.menu_log_verbosity_sub, 0, None, log_var)
        self.menu_log_verbosity_sub.add_radiobutton(label="(0) Error", variable=log_var, value=0)
        self.action_log_warning = (self.menu_log_verbosity_sub, 1, None, log_var)
        self.menu_log_verbosity_sub.add_radiobutton(label="(1) Warning", variable=log_var, value=1)
        self.action_log_info = (self.menu_log_verbosity_sub, 2, None, log_var)
        self.menu_log_verbosity_sub.add_radiobutton(label="(2) Info", variable=log_var, value=2)
        self.action_log_debug = (self.menu_log_verbosity_sub, 3, None, log_var)
        self.menu_log_verbosity_sub.add_radiobutton(label="(3) Debug", variable=log_var, value=3)
        self.menu_settings_sub.add_cascade(label="Log Verbosity", menu=self.menu_log_verbosity_sub)
        # === Help ===
        self.menu_help = (self.menubar, 2, None)
        self.menu_help_sub = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Hilfe", menu=self.menu_help_sub)
        # Show Help
        self.action_help = (self.menu_help_sub, 0, [None])
        self.menu_help_sub.add_command(label="Hilfe anzeigen")
        # About
        self.action_about_app = (self.menu_help_sub, 1, [None])
        self.menu_help_sub.add_command(label="Über YouTubeDownloader")

        # Statusbar
        #self.statusbar = Label(self, text="", bd=1, relief=SUNKEN, anchor=W)
        #self.statusbar.pack(side=BOTTOM, fill=X)
