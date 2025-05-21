"""!
********************************************************************************
@file   downloader.py
@brief  Download Thread
********************************************************************************
"""

import os
import re
import logging
from typing import TYPE_CHECKING
import statistics
import threading
import time
import pytubefix
from pytubefix import YouTube
from pytubefix.streams import Stream

from Source.version import __title__
from Source.Views.mainwindow_tk_ui import HIGH_RESOLUTION, LOW_RESOLUTION, ONLY_AUDIO
if TYPE_CHECKING:
    from Source.Controller.main_window import MainWindow

B_MP3_CONVERT = False

if B_MP3_CONVERT:
    from moviepy.editor import AudioFileClip

log = logging.getLogger(__title__)

S_DOWNLOAD_FOLDER = "Download"
I_SPEED_AVERAGE_VALUES = 10


class DownloadThread(threading.Thread):
    """!
    @brief Thread class for download
    @param main_controller : main controller
    """

    def __init__(self, main_controller: "MainWindow"):
        threading.Thread.__init__(self)
        self.main_controller = main_controller
        self.b_first_callback_call = False
        self.i_file_size = 0
        self.i_last_percent = 0
        self.f_time_stamp = 0.0
        self.i_last_bytes_remaining = 0
        self.l_speed_history: list[int] = []  # download speed history
        self.clear_data()

    def clear_data(self) -> None:
        """!
        @brief Clear data
        """
        self.b_first_callback_call = False
        self.i_file_size = 0
        self.i_last_percent = 0
        self.f_time_stamp = 0.0
        self.i_last_bytes_remaining = 0
        self.l_speed_history = []  # download speed history

    def run(self) -> None:
        """!
        @brief Download YouTube content
        """
        self.main_controller.status_lbl.configure(text="Analysiere URL...", text_color="grey")
        self.main_controller.progress_bar.set(0)
        i_choice = self.main_controller.choice_var.get()
        s_url = self.main_controller.o_url_choice.get()
        if i_choice != 0:
            l_url = []
            s_subfolder_name = ""
            if re.search("&list=", s_url):
                o_playlist = pytubefix.Playlist(s_url)
                s_subfolder_name = "/" + o_playlist.title
                for video in o_playlist.videos:
                    l_url.append(video.watch_url)
            else:
                l_url = [s_url]
            i_title_cnt = len(l_url)
            for i, s_url in enumerate(l_url, 1):
                self.main_controller.status_lbl.configure(text="Analysiere URL...", text_color="grey")
                s_text = f"Titel {i}/{i_title_cnt}: ..."
                self.main_controller.title_lbl.configure(text=s_text, text_color="orange")
                b_valid_url = False
                try:
                    o_youtube = YouTube(s_url, on_progress_callback=self.progress_callback)
                    s_titel = o_youtube.title[:35]
                    s_text = f"Titel {i}/{i_title_cnt}: {s_titel}"
                    self.main_controller.title_lbl.configure(text=s_text, text_color="orange")
                    b_valid_url = True
                except BaseException:  # pylint: disable=bare-except
                    self.main_controller.status_lbl.configure(text="Ungültige URL!", text_color="red")
                if b_valid_url:
                    self.clear_data()
                    s_filename = None
                    if i_choice == HIGH_RESOLUTION:
                        o_stream = o_youtube.streams.filter(progressive=True, file_extension='mp4')\
                            .get_highest_resolution()
                    elif i_choice == LOW_RESOLUTION:
                        o_stream = o_youtube.streams.filter(progressive=True, file_extension='mp4')\
                            .get_lowest_resolution()
                    elif i_choice == ONLY_AUDIO:
                        o_stream = o_youtube.streams.filter(only_audio=True).first()
                    else:
                        o_stream = None  # TODO
                        self.main_controller.status_lbl.configure(text="Unerwarteter Fehler!", text_color="red")
                    try:
                        self.main_controller.status_lbl.configure(text="Download läuft...", text_color="grey")
                        o_stream.download(S_DOWNLOAD_FOLDER + s_subfolder_name, s_filename)
                        self.main_controller.status_lbl.configure(text="Download abgeschlossen!", text_color="green")
                        if B_MP3_CONVERT:
                            if i_choice == ONLY_AUDIO:
                                self.main_controller.status_lbl.configure(text="MP3 wird erstellt...", text_color="grey")
                                s_file_path_name = S_DOWNLOAD_FOLDER + s_subfolder_name + "/" + o_stream.default_filename
                                audioclip = AudioFileClip(s_file_path_name)
                                audioclip.write_audiofile(s_file_path_name[:-1] + "3")
                                audioclip.close()
                                os.remove(s_file_path_name)
                                self.main_controller.status_lbl.configure(text="MP3 erstellt!", text_color="green")
                    except BaseException:  # pylint: disable=bare-except
                        self.main_controller.status_lbl.configure(text="Dieses Video kann nicht heruntergeladen werden!",
                                                                  text_color="red")
        else:
            self.main_controller.status_lbl.configure(text="Bitte Format angeben!", fg="red")
        self.main_controller.download_btn.configure(state="normal")
        self.main_controller.direct_btn.configure(state="normal")

    def progress_callback(self, _stream: Stream, _chunk: bytes, bytes_remaining: int) -> None:
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
            if self.f_time_stamp != 0:  # set calculate time only for second call
                i_actual_speed = int((self.i_last_bytes_remaining - bytes_remaining) / f_past_time)
                i_history_len = len(self.l_speed_history)
                if i_history_len < I_SPEED_AVERAGE_VALUES:
                    self.l_speed_history.append(i_actual_speed)
                else:
                    for i, value in enumerate(self.l_speed_history):
                        if i != 0:
                            self.l_speed_history[i - 1] = value
                    self.l_speed_history[I_SPEED_AVERAGE_VALUES - 1] = i_actual_speed
                i_average_speed = statistics.mean(self.l_speed_history)
                i_remaining_seconds = int(bytes_remaining / i_average_speed)
                self.main_controller.status_lbl.configure(text=f'Download läuft... noch {i_remaining_seconds}sek', text_color="grey")
            self.f_time_stamp = f_actual_time
            self.i_last_bytes_remaining = bytes_remaining
            i_percent = int(((self.i_file_size - bytes_remaining) / self.i_file_size) * 100)
            i_percent_diff = i_percent - self.i_last_percent
            for _ in range(i_percent_diff):
                self.main_controller.progress_bar.set(i_percent / 100)
            self.i_last_percent = i_percent


if __name__ == "__main__":
    my_url = "https://www.youtube.com/watch?v=QCRYA6ck3x0"
    try:
        my_youtube = YouTube(my_url)
    except BaseException:  # pylint: disable=bare-except
        print("Ungültige URL!")
    else:
        my_filename = None
        my_stream = my_youtube.streams.filter(only_audio=True).first()
        try:
            print("Download läuft...")
            my_stream.download(S_DOWNLOAD_FOLDER, my_filename)
            print("Download abgeschlossen!")
        except BaseException:  # pylint: disable=bare-except
            print("Dieses Video kann nicht heruntergeladen werden!")
