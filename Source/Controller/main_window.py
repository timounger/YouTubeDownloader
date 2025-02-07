"""!
********************************************************************************
@file   main_window.py
@brief  View controller for the main window
********************************************************************************
"""

import os
import logging
from typing import Any
import subprocess
from tkinter import Menu, Event
from customtkinter import CTk, CTkFont
from customtkinter.windows.widgets.ctk_entry import CTkEntry
from pytubefix import YouTube
import clipboard

from Source.Util.app_data import ICON_APP
from Source.version import __title__
from Source.Model.model import Model
from Source.Worker.downloader import DownloadThread

from Source.Views.mainwindow_tk_ui import Ui_MainWindow  # pylint: disable=wrong-import-position

from Source import version

log = logging.getLogger(__title__)

S_DOWNLOAD_FOLDER = "Download"
FONT_NAME = "Comic Sans MS"
FONT_SIZE = 14


def copy_selected_text_to_clipboard(url_input: CTkEntry) -> None:
    """!
    @brief Copy selected text to clipboard
    @param url_input : url
    """
    s_text = url_input.selection_get()
    clipboard.copy(s_text)


def delete_selected_text(url_input: CTkEntry) -> None:
    """!
    @brief Delete selected text
    @param url_input : url
    """
    try:
        s_select_text = url_input.selection_get()
    except BaseException:  # pylint: disable=bare-except
        pass
    else:
        s_entry_text = url_input.get()
        i_selected_text_length = len(s_select_text)
        i_curser_pos = url_input.index('insert')
        i_curser_pos_end = i_curser_pos + i_selected_text_length
        s_text_to_check = s_entry_text[i_curser_pos: i_curser_pos_end]
        if s_text_to_check == s_select_text:
            url_input.delete(i_curser_pos, i_curser_pos_end)
        else:
            url_input.delete(i_curser_pos - i_selected_text_length, i_curser_pos)


class MainWindow(CTk, Ui_MainWindow):
    """!
    @brief Class for YouTube download GUI
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=keyword-arg-before-vararg
        log.debug("Initializing Main Window")
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.title(__title__)
        self.wm_iconbitmap(ICON_APP)  # set icon
        self.geometry("350x360")  # set window
        self.resizable(0, 0)  # Don't allow resizing
        self.columnconfigure(0, weight=1)  # set all content in center.
        # init widgets
        self.init_widgets()
        self.model = Model(self)
        self.model.c_monitor.update_darkmode_status(self.model.c_monitor.e_style)

    def init_widgets(self) -> None:
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
        self.url_input.configure(placeholder_text="Gebe die YouTube URL ein:")
        # Entry Box
        s_clipboard_text = clipboard.paste()  # get content of clip board
        s_compare_string = "https://"
        b_valid_url = False
        if s_clipboard_text[0:len(s_compare_string)] == s_compare_string:
            try:
                YouTube(s_clipboard_text)
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
        self.insert_btn.configure(text="Einfügen", fg_color="green", text_color="white", command=self.input_link)
        self.direct_btn.configure(text="Direkt Download", fg_color="darkorange", text_color="white", command=self.direct_clicked)
        # Error Message
        self.status_lbl.configure(text=s_default_status, text_color="grey", font=CTkFont(family=FONT_NAME, size=FONT_SIZE))
        # Title Message
        self.title_lbl.configure(text="Aktueller Song", text_color="orange", font=CTkFont(family=FONT_NAME, size=FONT_SIZE))
        # format label
        self.format_lbl.configure(text="Wähle ein Format:", font=CTkFont(size=FONT_SIZE))
        # download button
        self.download_btn.configure(text="Download", fg_color="red", text_color="white", command=self.start_download)
        # folder button
        self.open_folder_btn.configure(text="Öffne Speicherort", fg_color="grey", text_color="white")
        # developer Label
        self.copyright_lbl.configure(text=version.__copyright__, font=CTkFont(family=FONT_NAME, size=FONT_SIZE))

    def copy(self) -> None:
        """!
        @brief Copy selected text to clipboard
        """
        copy_selected_text_to_clipboard(self.url_input)

    def cut(self) -> None:
        """!
        @brief Copy selected text to clipboard and cut text out
        """
        copy_selected_text_to_clipboard(self.url_input)
        delete_selected_text(self.url_input)

    def paste(self) -> None:
        """!
        @brief Paste text from clipboard to position
        """
        delete_selected_text(self.url_input)
        self.url_input.insert(self.url_input.index('insert'), clipboard.paste())  # paste at cursor position

    def do_popup(self, event: Event) -> None:
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

    def input_link(self) -> None:
        """!
        @brief Input text from clipboard to entry box
        """
        self.url_input.delete(0, "end")
        self.url_input.insert(0, clipboard.paste())  # paste content of clipboard
        self.status_lbl.configure(text="Text aus Zwischenablage wurde eingefügt!", text_color="grey")

    def direct_clicked(self) -> None:
        """!
        @brief direct download clicked
        """
        self.input_link()
        self.start_download()

    def start_download(self) -> None:
        """!
        @brief Create and start thread for download
        """
        self.download_btn.configure(state="disabled")
        self.direct_btn.configure(state="disabled")
        c_download = DownloadThread(self)
        c_download.start()

    def open_download_folder(self) -> None:
        """!
        @brief Open download folder and create if not exist
        """
        if not os.path.isdir(S_DOWNLOAD_FOLDER):
            os.makedirs(S_DOWNLOAD_FOLDER)
        with subprocess.Popen('explorer ' + S_DOWNLOAD_FOLDER):
            pass
