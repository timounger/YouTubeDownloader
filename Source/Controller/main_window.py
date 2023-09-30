# This Python file uses the following encoding: utf-8
"""
*****************************************************************************
 @file    main_window.py
 @brief   YouTube content download
*****************************************************************************
"""

import os
from tkinter import Label, Tk, StringVar, IntVar, Entry, Radiobutton, Button, Menu
from tkinter.ttk import Progressbar, Style
import subprocess
import clipboard
import pytube

import Source.Util.downloader_data as mdata
from Source.Worker.downloader import DownloadThread

from Source import version

S_DOWNLOAD_FOLDER = "Download"

L_FORMAT = [
    ("Hohe Auflösung", 1),
    ("Niedrige Auflösung", 2),
    ("Nur Audio", 3)
]

def copy_selected_text_to_clipboard(o_url):
    """!
    @brief Copy selected text to clipboard
    @param o_url : url
    """
    s_text = o_url.selection_get()
    clipboard.copy(s_text)

def delete_selected_text(o_url):
    """!
    @brief Delete selected text
    @param o_url : url
    """
    try:
        s_select_text = o_url.selection_get()
    except: # pylint: disable=bare-except
        pass
    else:
        s_enty_text = o_url.get()
        i_selected_text_length = len(s_select_text)
        i_curser_pos = o_url.index('insert')
        i_curser_pos_end = i_curser_pos + i_selected_text_length
        s_text_to_check = s_enty_text[i_curser_pos : i_curser_pos_end]
        if s_text_to_check == s_select_text:
            o_url.delete(i_curser_pos, i_curser_pos_end)
        else:
            o_url.delete(i_curser_pos - i_selected_text_length, i_curser_pos)

class YoutubeDownloader:
    """!
    @brief Class for YouTube download GUI
    """
    def __init__(self): # pylint: disable=R0914
        self.root = Tk()
        self.root.title(version.__title__ + f" v{version.__version__}")
        self.root.wm_iconbitmap(mdata.S_ICON_REL_PATH) # set icon
        self.root.geometry("350x320") #set window
        self.root.resizable(0, 0) # Don't allow resizing
        self.root.columnconfigure(0, weight=1) #set all content in center.
        self.o_url_choice = StringVar()
        self.o_format_choice = IntVar()
        #YouTube Link Label
        o_url_label = Label(self.root,text="Gebe die YouTube URL ein:",font=("jost",15))
        o_url_label.grid()
        #Entry Box
        self.o_url = Entry(self.root,width=50,textvariable=self.o_url_choice)
        self.o_url.bind("<Button-3>", self.do_popup) # event for right mouse click (button 3)
        s_clipboard_text = clipboard.paste() # get content of clip board
        s_compare_string = "https://"
        b_valid_url = False
        if s_clipboard_text[0:len(s_compare_string)] == s_compare_string:
            try:
                pytube.YouTube(s_clipboard_text)
                b_valid_url = True
            except: # pylint: disable=bare-except
                b_valid_url = False
        if b_valid_url:
            s_default_text = s_clipboard_text
            s_default_status = "URL aus Zwischenablage wurde eingefügt!"
        else:
            s_default_text = "" # if no YouTube link or invalid set no text as default
            s_default_status = "URL eingeben und Download starten!"
        self.o_url.insert(0, s_default_text) # set content of clipboard as default
        self.o_url.grid()
        o_input_button = Button(self.root,text="Einfügen",width=10,\
                                bg="green",fg="white",command=self.input_link)
        o_input_button.grid()
        #Error Message
        self.o_status = Label(self.root,text=s_default_status,fg="blue",font=("jost",10))
        self.o_status.grid()
        # Title Message
        self.o_titel = Label(self.root,text="Aktueller Song",fg="orange",font=("jost",10))
        self.o_titel.grid()
        # progress bar
        self.style = Style(self.root)
        self.style.layout('text.Horizontal.TProgressbar',
                     [('Horizontal.Progressbar.trough',
                       {'children': [('Horizontal.Progressbar.pbar',
                                      {'side': 'left', 'sticky': 'ns'})],
                        'sticky': 'nswe'}),
                      ('Horizontal.Progressbar.label', {'sticky': ''})])
        self.style.configure('text.Horizontal.TProgressbar', text='0 %')
        self.o_progress = Progressbar(self.root,style='text.Horizontal.TProgressbar',\
                                      length=200,  maximum=100, value=0,)
        self.o_progress.grid()
        # format label
        o_format_label = Label(self.root,text="Wähle ein Format:",font=("jost",14))
        o_format_label.grid()
        # format radio button
        for txt, val in L_FORMAT:
            o_format = Radiobutton(self.root, text=txt, padx = 20,\
                                   variable = self.o_format_choice, value=val)
            o_format.grid()
        self.o_format_choice.set(1) # set first radio button as default
        #download button
        self.o_download_button = Button(self.root,text="Download",width=10,\
                                   bg="red",fg="white",command=self.start_download)
        self.o_download_button.grid()
        #folder button
        o_folder_button = Button(self.root,text="Öffne Speicherort",width=15,\
                                   bg="grey",fg="white",command=self.open_download_folder)
        o_folder_button.grid()
        #developer Label
        o_developer_label = Label(self.root,text=version.__copyright__,font=("Calibri",12))
        o_developer_label.grid()
        # right click content menu
        self.menu = Menu(self.root, tearoff = 0)
        self.menu.add_command(label ="Ausschneiden", command=self.cut)
        self.menu.add_command(label ="Kopieren", command=self.copy)
        self.menu.add_command(label ="Einfügen", command=self.paste)

    def copy(self):
        """!
        @brief Copy selected text to clipboard
        """
        copy_selected_text_to_clipboard(self.o_url)

    def cut(self):
        """!
        @brief Copy selected text to clipboard and cut text out
        """
        copy_selected_text_to_clipboard(self.o_url)
        delete_selected_text(self.o_url)

    def paste(self):
        """!
        @brief Paste text from clipboard to position
        """
        delete_selected_text(self.o_url)
        self.o_url.insert(self.o_url.index('insert'), clipboard.paste()) # paste at cursor position

    def do_popup(self, event):
        """!
        @brief Pop up content menu
        @param event : arrived event
        """
        try:
            self.o_url.selection_get()
            self.menu.entryconfig("Kopieren", state="normal")
            self.menu.entryconfig("Ausschneiden", state="normal")
        except: # pylint: disable=bare-except
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
        self.o_url.delete(0, "end")
        self.o_url.insert(0, clipboard.paste()) # paste content of clipboard
        self.o_status.config(text="Text aus Zwischenablage wurde eingefügt!",fg="blue")

    def start_download(self):
        """!
        @brief Create and start thread for download
        """
        self.o_download_button["state"] = "disable"
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
