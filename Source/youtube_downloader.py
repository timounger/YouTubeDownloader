# This Python file uses the following encoding: utf-8
"""
*****************************************************************************
 @file    youtube_downloader.py
 @brief   YouTube content download
*****************************************************************************
"""

import os
import sys
from tkinter import Label, Tk, StringVar, IntVar, Entry, Radiobutton, Button, Menu
from tkinter.ttk import Progressbar, Style
import statistics
import subprocess
import threading
import time
import re
import ctypes
import clipboard
import pytube
from moviepy.editor import AudioFileClip

sys.path.append('../')
import Source.downloader_data as mdata # pylint: disable=wrong-import-position

S_DOWNLOAD_FOLDER = "Download"
I_SPEED_AVERAGE_VALUES = 10

L_FORMAT = [
    ("Hohe Auflösung", 1),
    ("Niedrige Auflösung", 2),
    ("Nur Audio", 3)
]

class DownloadThread(threading.Thread):
    """!
    @brief Thread class for download
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.b_first_callback_call = False
        self.i_file_size = 0
        self.i_last_percent = 0
        self.f_time_stamp = 0.0
        self.i_last_bytes_remaining = 0
        self.d_speed_history = [] # download speed history
        self.clear_data()

    def clear_data(self):
        """!
        @brief Clear data
        """
        self.b_first_callback_call = False
        self.i_file_size = 0
        self.i_last_percent = 0
        self.f_time_stamp = 0.0
        self.i_last_bytes_remaining = 0
        self.d_speed_history = [] # download speed history

    def run(self):
        """!
        @brief Download YouTube content
        """
        gui.o_status.config(text="Analysiere URL...", fg="blue")
        i_choice = gui.o_format_choice.get()
        s_url = gui.o_url_choice.get()
        if  i_choice != 0:
            l_url = []
            s_subfolder_name = ""
            if re.search("&list=", s_url):
                o_playlist = pytube.Playlist(s_url)
                s_subfolder_name = "/" + o_playlist.title
                for video in o_playlist.videos:
                    l_url.append(video.watch_url)
            else:
                l_url = [s_url]
            i_titels = len(l_url)
            for i, s_url in enumerate(l_url, 1):
                gui.o_status.config(text="Analysiere URL...", fg="blue")
                s_text = f"Titel {i}/{i_titels}: ..."
                gui.o_titel.config(text=s_text,fg="orange")
                b_valid_url = False
                try:
                    o_youtube = pytube.YouTube(s_url, on_progress_callback=self.progress_callback)
                    s_titel = o_youtube.title[:35]
                    s_text = f"Titel {i}/{i_titels}: {s_titel}"
                    gui.o_titel.config(text=s_text,fg="orange")
                    b_valid_url = True
                except: # pylint: disable=bare-except
                    gui.o_status.config(text="Ungültige URL!",fg="red")
                if b_valid_url:
                    self.clear_data()
                    s_filename = None
                    if i_choice == 1:
                        o_stream = o_youtube.streams.filter(progressive=True, file_extension='mp4')\
                                                             .get_highest_resolution()
                    elif i_choice == 2:
                        o_stream = o_youtube.streams.filter(progressive=True, file_extension='mp4')\
                                                             .get_lowest_resolution()
                    elif i_choice == 3:
                        o_stream = o_youtube.streams.filter(only_audio=True).first()
                    else:
                        gui.o_status.config(text="Unerwarteter Fehler!",fg="red")
                    try:
                        gui.o_status.config(text="Download läuft...", fg="blue")
                        o_stream.download(S_DOWNLOAD_FOLDER + s_subfolder_name, s_filename)
                        gui.o_status.config(text="Download abgeschlossen!", fg="green")
                        if i_choice == 3:
                            gui.o_status.config(text="MP3 wird erstellt...", fg="blue")
                            s_file_path_name = S_DOWNLOAD_FOLDER + s_subfolder_name + "/" + o_stream.default_filename
                            audioclip = AudioFileClip(s_file_path_name)
                            audioclip.write_audiofile(s_file_path_name[:-1] + "3")
                            audioclip.close()
                            os.remove(s_file_path_name)
                            gui.o_status.config(text="MP3 erstellt!", fg="green")
                    except: # pylint: disable=bare-except
                        gui.o_status.config(text="Dieses Video kann nicht heruntergeladen werden!",\
                                              fg="red")
        else:
            gui.o_status.config(text="Bitte Format angeben!",fg="red")
        gui.o_download_button["state"] = "normal"

    def progress_callback(self, _stream, _chunk, bytes_remaining):
        """!
        @brief Calculate process and update process bar
        @param _stream : stream
        @param _chunk : chunk
        @param bytes_remaining : bytes remaining
        """
        if not self.b_first_callback_call:
            self.i_file_size = bytes_remaining
            self.i_last_bytes_remaining = bytes_remaining
            self.b_first_callback_call = True
        else:
            f_actual_time = time.time()
            f_past_time = f_actual_time - self.f_time_stamp
            if self.f_time_stamp != 0: # set calculate time only for second call
                i_actual_speed = int((self.i_last_bytes_remaining - bytes_remaining) / f_past_time)
                i_history_len = len(self.d_speed_history)
                if i_history_len < I_SPEED_AVERAGE_VALUES:
                    self.d_speed_history.append(i_actual_speed)
                else:
                    for i, value in enumerate(self.d_speed_history):
                        if i != 0:
                            self.d_speed_history[i-1] = value
                    self.d_speed_history[I_SPEED_AVERAGE_VALUES-1] = i_actual_speed
                i_average_speed = statistics.mean(self.d_speed_history)
                i_remaining_seconds = int(bytes_remaining / i_average_speed)
                gui.o_status.config(text=f'Download läuft... noch {i_remaining_seconds}sek', fg="blue")
            self.f_time_stamp = f_actual_time
            self.i_last_bytes_remaining = bytes_remaining
            i_percent = int(((self.i_file_size - bytes_remaining) / self.i_file_size) * 100)
            i_percent_diff = i_percent - self.i_last_percent
            for _ in range(i_percent_diff):
                gui.o_progress.step()
            gui.style.configure('text.Horizontal.TProgressbar', text=f'{i_percent}%')
            self.i_last_percent = i_percent

class YoutubeDownloader:
    """!
    @brief Class for YouTube download GUI
    """
    def __init__(self): # pylint: disable=R0914
        self.root = Tk()
        self.root.title(mdata.S_YOUTUBE_DOWNLOADER_APPLICATION_NAME + f" v{mdata.S_VERSION}\n")
        self.root.wm_iconbitmap(mdata.S_ICON_REL_PATH) # set icon
        self.root.geometry("350x300") #set window
        self.root.resizable(0, 0) # Don't allow resizing
        self.root.columnconfigure(0,weight=1) #set all content in center.
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
            s_default_status = "URL eingeben und Downlaod starten!"
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
        o_developer_label = Label(self.root,text=mdata.S_COPYRIGHT,font=("Calibri",12))
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
        c_download = DownloadThread()
        c_download.start()

    def open_download_folder(self):
        """!
        @brief Open download folder and create if not exist
        """
        if not os.path.isdir(S_DOWNLOAD_FOLDER):
            os.makedirs(S_DOWNLOAD_FOLDER)
        with subprocess.Popen('explorer ' + S_DOWNLOAD_FOLDER):
            pass

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

if __name__ == "__main__":
    # Set custom application id to show correct icon instead of Python in the task bar
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(mdata.S_APP_ID)
    except ImportError:
        pass

    gui = YoutubeDownloader()
    gui.root.mainloop()
    