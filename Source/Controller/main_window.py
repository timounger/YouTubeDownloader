"""!
********************************************************************************
@file   main_window.py
@brief  View controller for the main window.
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

from Source.Util.app_data import ICON_APP, DOWNLOAD_FOLDER
from Source.version import __title__
from Source.Model.model import Model
from Source.Worker.downloader import DownloadThread

from Source.Views.mainwindow_tk_ui import Ui_MainWindow  # pylint: disable=wrong-import-position

from Source import version

log = logging.getLogger(__title__)

FONT_NAME = "Comic Sans MS"
FONT_SIZE = 14


def copy_selected_text_to_clipboard(url_input: CTkEntry) -> None:
    """!
    @brief Copy the currently selected text in the entry field to the system clipboard.
    @param url_input : entry widget containing the text selection
    """
    text = url_input.selection_get()
    clipboard.copy(text)


def delete_selected_text(url_input: CTkEntry) -> None:
    """!
    @brief Delete the currently selected text from the entry field.
    @param url_input : entry widget containing the text selection
    """
    try:
        selected_text = url_input.selection_get()
    except Exception:
        pass
    else:
        entry_text = url_input.get()
        selection_length = len(selected_text)
        cursor_pos = url_input.index('insert')
        cursor_pos_end = cursor_pos + selection_length
        text_at_cursor = entry_text[cursor_pos:cursor_pos_end]
        if text_at_cursor == selected_text:
            url_input.delete(cursor_pos, cursor_pos_end)
        else:
            url_input.delete(cursor_pos - selection_length, cursor_pos)


class MainWindow(CTk, Ui_MainWindow):  # type: ignore[misc]
    """!
    @brief Main application window for the YouTube download GUI.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=keyword-arg-before-vararg
        log.debug("Initializing Main Window")
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.title(__title__)
        self.wm_iconbitmap(ICON_APP)
        self.geometry("350x360")
        self.resizable(False, False)
        self.columnconfigure(0, weight=1)
        self.init_widgets()
        self.model = Model(self)
        self.model.monitor.apply_theme(self.model.monitor.selected_theme)

    def init_widgets(self) -> None:
        """!
        @brief Configure widget texts, colors, fonts and event bindings.
        """
        # right click context menu
        context_menu_items = {
            "Ausschneiden": self.cut,
            "Kopieren": self.copy,
            "Einfügen": self.paste
        }
        self.menu = Menu(self, tearoff=0)
        for text, callback in context_menu_items.items():
            self.menu.add_command(label=text, command=callback)
        self.url_input.bind("<Button-3>", self.show_context_menu)
        self.url_input.configure(placeholder_text="Gebe die YouTube URL ein:")
        # Entry Box
        clipboard_text = clipboard.paste()
        valid_url = False
        if clipboard_text.startswith("https://"):
            try:
                YouTube(clipboard_text)
                valid_url = True
            except Exception:
                valid_url = False
        if valid_url:
            default_text = clipboard_text
            default_status = "URL aus Zwischenablage wurde eingefügt!"
        else:
            default_text = ""
            default_status = "URL eingeben und Download starten!"
        self.url_input.insert(0, default_text)
        self.insert_btn.configure(text="Einfügen", fg_color="green", text_color="white", command=self.paste_from_clipboard)
        self.direct_btn.configure(text="Direkt Download", fg_color="darkorange", text_color="white", command=self.paste_and_download)
        # Status Message
        self.status_lbl.configure(text=default_status, text_color="grey", font=CTkFont(family=FONT_NAME, size=FONT_SIZE))
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
        @brief Copy selected text from the URL input to the system clipboard.
        """
        copy_selected_text_to_clipboard(self.url_input)

    def cut(self) -> None:
        """!
        @brief Cut selected text from the URL input to the system clipboard.
        """
        copy_selected_text_to_clipboard(self.url_input)
        delete_selected_text(self.url_input)

    def paste(self) -> None:
        """!
        @brief Paste text from the system clipboard at the current cursor position.
        """
        delete_selected_text(self.url_input)
        self.url_input.insert(self.url_input.index('insert'), clipboard.paste())

    def show_context_menu(self, event: Event) -> None:
        """!
        @brief Display the right-click context menu at the mouse position.
        @param event : mouse event containing the click coordinates
        """
        try:
            self.url_input.selection_get()
            self.menu.entryconfig("Kopieren", state="normal")
            self.menu.entryconfig("Ausschneiden", state="normal")
        except Exception:
            self.menu.entryconfig("Kopieren", state="disabled")
            self.menu.entryconfig("Ausschneiden", state="disabled")
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def paste_from_clipboard(self) -> None:
        """!
        @brief Replace the URL input content with the current clipboard text.
        """
        self.url_input.delete(0, "end")
        self.url_input.insert(0, clipboard.paste())
        self.status_lbl.configure(text="Text aus Zwischenablage wurde eingefügt!", text_color="grey")

    def paste_and_download(self) -> None:
        """!
        @brief Paste clipboard content into URL input and immediately start the download.
        """
        self.paste_from_clipboard()
        self.start_download()

    def start_download(self) -> None:
        """!
        @brief Create and start a background thread for the download process.
        """
        self.download_btn.configure(state="disabled")
        self.direct_btn.configure(state="disabled")
        download = DownloadThread(self)
        download.start()

    def open_download_folder(self) -> None:
        """!
        @brief Open the download folder in the file explorer, creating it if necessary.
        """
        if not os.path.isdir(DOWNLOAD_FOLDER):
            os.makedirs(DOWNLOAD_FOLDER)
        with subprocess.Popen(['explorer', DOWNLOAD_FOLDER]):
            pass
