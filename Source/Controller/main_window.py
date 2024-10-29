"""!
********************************************************************************
@file   main_window.py
@brief  View controller for the main window
********************************************************************************
"""

import os
from tkinter import Tk, Menu
import subprocess
import clipboard
import pytube

from Source.Util.app_data import S_ICON_REL_PATH
from Source.version import __title__
from Source.Model.model import Model
from Source.Worker.downloader import DownloadThread

from Source.Views.mainwindow_tk_ui import Ui_MainWindow  # pylint: disable=wrong-import-position
from Source.Views.dialogs.dialog_splash_ui_tk import Ui_SplashScreen  # pylint: disable=wrong-import-position
from Source.Views.dialogs.dialog_about_ui_tk import Ui_AboutDialog  # pylint: disable=wrong-import-position
from Source.Views.dialogs.dialog_help_ui_tk import Ui_HelpDialog  # pylint: disable=wrong-import-position

from Source import version

S_DOWNLOAD_FOLDER = "Download"


def copy_selected_text_to_clipboard(url_input):
    """!
    @brief Copy selected text to clipboard
    @param url_input : url
    """
    s_text = url_input.selection_get()
    clipboard.copy(s_text)


def delete_selected_text(url_input):
    """!
    @brief Delete selected text
    @param url_input : url
    """
    try:
        s_select_text = url_input.selection_get()
    except BaseException:  # pylint: disable=bare-except
        pass
    else:
        s_enty_text = url_input.get()
        i_selected_text_length = len(s_select_text)
        i_curser_pos = url_input.index('insert')
        i_curser_pos_end = i_curser_pos + i_selected_text_length
        s_text_to_check = s_enty_text[i_curser_pos: i_curser_pos_end]
        if s_text_to_check == s_select_text:
            url_input.delete(i_curser_pos, i_curser_pos_end)
        else:
            url_input.delete(i_curser_pos - i_selected_text_length, i_curser_pos)


class MainWindow(Tk, Ui_MainWindow):
    """!
    @brief Class for YouTube download GUI
    """

    def __init__(self, *args, **kwargs):  # pylint: disable=keyword-arg-before-vararg
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.title(__title__)
        self.wm_iconbitmap(S_ICON_REL_PATH)  # set icon
        self.geometry("350x320")  # set window
        self.resizable(0, 0)  # Don't allow resizing
        self.columnconfigure(0, weight=1)  # set all content in center.
        # init widgets
        self.init_widgets()
        self.model = Model(self)
        self.model.c_monitor.update_darkmode_status(self.model.c_monitor.e_style)

    def init_widgets(self):
        """!
        @brief Initialize widgets
        """
        # right click content menu
        d_context = {
            "Ausschneiden": self.cut,
            "Kopieren": self.copy,
            "Einfügen": self.paste
        }
        self.menu = Menu(self, tearoff=0)
        for text, callback in d_context.items():
            self.menu.add_command(label=text, command=callback)
        self.url_input.bind("<Button-3>", self.do_popup)  # event for right mouse click (button 3)
        # YouTube Link Label
        self.url_lbl.config(text="Gebe die YouTube URL ein:", font=("jost", 15))
        # Entry Box
        s_clipboard_text = clipboard.paste()  # get content of clip board
        s_compare_string = "https://"
        b_valid_url = False
        if s_clipboard_text[0:len(s_compare_string)] == s_compare_string:
            try:
                pytube.YouTube(s_clipboard_text)
                b_valid_url = True
            except BaseException:  # pylint: disable=bare-except
                b_valid_url = False
        if b_valid_url:
            s_default_text = s_clipboard_text
            s_default_status = "URL aus Zwischenablage wurde eingefügt!"
        else:
            s_default_text = ""  # if no YouTube link or invalid set no text as default
            s_default_status = "URL eingeben und Download starten!"
        self.url_input.insert(0, s_default_text)  # set content of clipboard as default
        self.insert_btn.config(text="Einfügen", bg="green", fg="white", command=self.input_link)
        # Error Message
        self.status_lbl.config(text=s_default_status, fg="blue", font=("jost", 10))
        # Title Message
        self.title_lbl.config(text="Aktueller Song", fg="orange", font=("jost", 10))
        # format label
        self.formal_lbl.config(text="Wähle ein Format:", font=("jost", 14))
        # download button
        self.download_btn.config(text="Download", bg="red", fg="white", command=self.start_download)
        # folder button
        self.open_folder_btn.config(text="Öffne Speicherort", bg="grey", fg="white")
        # developer Label
        self.copyright_lbl.config(text=version.__copyright__, font=("Calibri", 12))

    def copy(self):
        """!
        @brief Copy selected text to clipboard
        """
        copy_selected_text_to_clipboard(self.url_input)

    def cut(self):
        """!
        @brief Copy selected text to clipboard and cut text out
        """
        copy_selected_text_to_clipboard(self.url_input)
        delete_selected_text(self.url_input)

    def paste(self):
        """!
        @brief Paste text from clipboard to position
        """
        delete_selected_text(self.url_input)
        self.url_input.insert(self.url_input.index('insert'), clipboard.paste())  # paste at cursor position

    def do_popup(self, event):
        """!
        @brief Pop up content menu
        @param event : arrived event
        """
        try:
            self.url_input.selection_get()
            self.menu.entryconfig("Kopieren", state="normal")
            self.menu.entryconfig("Ausschneiden", state="normal")
        except BaseException:  # pylint: disable=bare-except
            self.menu.entryconfig("Kopieren", state="disabled")
            self.menu.entryconfig("Ausschneiden", state="disabled")
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def input_link(self):
        """!
        @brief Input text from clipboard to entry box
        """
        self.url_input.delete(0, "end")
        self.url_input.insert(0, clipboard.paste())  # paste content of clipboard
        self.status_lbl.config(text="Text aus Zwischenablage wurde eingefügt!", fg="blue")

    def start_download(self):
        """!
        @brief Create and start thread for download
        """
        self.download_btn["state"] = "disable"
        c_download = DownloadThread(self)
        c_download.start()

    def open_download_folder(self):
        """!
        @brief Open download folder and create if not exist
        """
        if not os.path.isdir(S_DOWNLOAD_FOLDER):
            os.makedirs(S_DOWNLOAD_FOLDER)
        with subprocess.Popen('explorer ' + S_DOWNLOAD_FOLDER):
            pass
