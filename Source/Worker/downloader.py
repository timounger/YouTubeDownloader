"""!
********************************************************************************
@file   downloader.py
@brief  Background thread for downloading YouTube videos and audio.
********************************************************************************
"""

import os
import re
import logging
from typing import TYPE_CHECKING
from collections import deque
import statistics
import threading
import time
import pytubefix
from pytubefix import YouTube
from pytubefix.streams import Stream

from Source.version import __title__
from Source.Util.app_data import DOWNLOAD_FOLDER
from Source.Views.mainwindow_tk_ui import HIGH_RESOLUTION, LOW_RESOLUTION, ONLY_AUDIO
if TYPE_CHECKING:
    from Source.Controller.main_window import MainWindow

B_MP3_CONVERT = False

if B_MP3_CONVERT:
    from moviepy.editor import AudioFileClip

log = logging.getLogger(__title__)

SPEED_AVERAGE_VALUES = 10


class DownloadThread(threading.Thread):
    """!
    @brief Thread that downloads YouTube content and updates the UI progress.
    @param main_controller : main window controller providing UI access
    """

    def __init__(self, main_controller: "MainWindow"):
        threading.Thread.__init__(self)
        self.main_controller = main_controller
        self.first_callback_call = False
        self.file_size = 0
        self.last_percent = 0
        self.timestamp = 0.0
        self.last_bytes_remaining = 0
        self.speed_history: deque[int] = deque(maxlen=SPEED_AVERAGE_VALUES)
        self.reset_progress_state()

    def reset_progress_state(self) -> None:
        """!
        @brief Reset all download progress tracking variables to initial state.
        """
        self.first_callback_call = False
        self.file_size = 0
        self.last_percent = 0
        self.timestamp = 0.0
        self.last_bytes_remaining = 0
        self.speed_history.clear()

    def run(self) -> None:
        """!
        @brief Execute the download process for a single video or playlist.
        """
        self.main_controller.status_lbl.configure(text="Analysiere URL...", text_color="grey")
        self.main_controller.progress_bar.set(0)
        choice = self.main_controller.choice_var.get()
        url = self.main_controller.url_choice.get()
        if choice != 0:
            urls: list[str] = []
            subfolder_name = ""
            if re.search("&list=", url):
                playlist = pytubefix.Playlist(url)
                subfolder_name = f"/{playlist.title}"
                for video in playlist.videos:
                    urls.append(video.watch_url)
            else:
                urls = [url]
            title_count = len(urls)
            for index, url in enumerate(urls, 1):
                self.main_controller.status_lbl.configure(text="Analysiere URL...", text_color="grey")
                text = f"Titel {index}/{title_count}: ..."
                self.main_controller.title_lbl.configure(text=text, text_color="orange")
                valid_url = False
                try:
                    youtube = YouTube(url, on_progress_callback=self.progress_callback)
                    title = youtube.title[:35]
                    text = f"Titel {index}/{title_count}: {title}"
                    self.main_controller.title_lbl.configure(text=text, text_color="orange")
                    valid_url = True
                except Exception:
                    self.main_controller.status_lbl.configure(text="Ungültige URL!", text_color="red")
                if valid_url:
                    self.reset_progress_state()
                    self.download_stream(youtube, choice, subfolder_name)
        else:
            self.main_controller.status_lbl.configure(text="Bitte Format angeben!", text_color="red")
        self.main_controller.download_btn.configure(state="normal")
        self.main_controller.direct_btn.configure(state="normal")

    def download_stream(self, youtube: YouTube, choice: int, subfolder_name: str) -> None:
        """!
        @brief Download a single YouTube stream based on the selected format.
        @param youtube : YouTube object for the video to download
        @param choice : format selection (HIGH_RESOLUTION, LOW_RESOLUTION, ONLY_AUDIO)
        @param subfolder_name : optional subfolder for playlist downloads
        """
        filename = None
        if choice == HIGH_RESOLUTION:
            stream = youtube.streams.filter(progressive=True, file_extension='mp4') \
                .get_highest_resolution()
        elif choice == LOW_RESOLUTION:
            stream = youtube.streams.filter(progressive=True, file_extension='mp4') \
                .get_lowest_resolution()
        elif choice == ONLY_AUDIO:
            stream = youtube.streams.filter(only_audio=True).first()
        else:
            stream = None  # TODO
            self.main_controller.status_lbl.configure(text="Unerwarteter Fehler!", text_color="red")
        try:
            self.main_controller.status_lbl.configure(text="Download läuft...", text_color="grey")
            stream.download(f"{DOWNLOAD_FOLDER}{subfolder_name}", filename)
            self.main_controller.status_lbl.configure(text="Download abgeschlossen!", text_color="green")
            if B_MP3_CONVERT:
                if choice == ONLY_AUDIO:
                    self.main_controller.status_lbl.configure(text="MP3 wird erstellt...", text_color="grey")
                    file_path = f"{DOWNLOAD_FOLDER}{subfolder_name}/{stream.default_filename}"
                    audioclip = AudioFileClip(file_path)
                    audioclip.write_audiofile(f"{file_path[:-1]}3")
                    audioclip.close()
                    os.remove(file_path)
                    self.main_controller.status_lbl.configure(text="MP3 erstellt!", text_color="green")
        except Exception:
            self.main_controller.status_lbl.configure(text="Dieses Video kann nicht heruntergeladen werden!",
                                                      text_color="red")

    def progress_callback(self, _stream: Stream, _chunk: bytes, bytes_remaining: int) -> None:
        """!
        @brief Callback for download progress updates. Calculates speed and remaining time.
        @param _stream : the stream being downloaded (unused)
        @param _chunk : the last downloaded data chunk (unused)
        @param bytes_remaining : number of bytes still to be downloaded
        """
        if not self.first_callback_call:
            self.file_size = bytes_remaining
            self.last_bytes_remaining = bytes_remaining
            self.first_callback_call = True
        else:
            current_time = time.time()
            elapsed_time = current_time - self.timestamp
            if self.timestamp != 0:
                current_speed = int((self.last_bytes_remaining - bytes_remaining) / elapsed_time)
                self.speed_history.append(current_speed)
                average_speed = statistics.mean(self.speed_history)
                remaining_seconds = int(bytes_remaining / average_speed)
                self.main_controller.status_lbl.configure(
                    text=f"Download läuft... noch {remaining_seconds}sek", text_color="grey")
            self.timestamp = current_time
            self.last_bytes_remaining = bytes_remaining
            percent = int(((self.file_size - bytes_remaining) / self.file_size) * 100)
            self.main_controller.progress_bar.set(percent / 100)
            self.last_percent = percent


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
            my_stream.download(DOWNLOAD_FOLDER, my_filename)
            print("Download abgeschlossen!")
        except BaseException:  # pylint: disable=bare-except
            print("Dieses Video kann nicht heruntergeladen werden!")
