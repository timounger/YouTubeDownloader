"""!
********************************************************************************
@file    downloader.py
@brief   Download Thread
********************************************************************************
"""

import os
import statistics
import threading
import time
import re
import pytube

B_MP3_CONVERT = False

if B_MP3_CONVERT:
    from moviepy.editor import AudioFileClip

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
    @param main_controller : main controller
    """

    def __init__(self, main_controller):
        threading.Thread.__init__(self)
        self.main_controller = main_controller
        self.b_first_callback_call = False
        self.i_file_size = 0
        self.i_last_percent = 0
        self.f_time_stamp = 0.0
        self.i_last_bytes_remaining = 0
        self.l_speed_history = []  # download speed history
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
        self.l_speed_history = []  # download speed history

    def run(self):
        """!
        @brief Download YouTube content
        """
        self.main_controller.o_status.config(text="Analysiere URL...", fg="blue")
        i_choice = self.main_controller.o_format_choice.get()
        s_url = self.main_controller.o_url_choice.get()
        if i_choice != 0:
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
                self.main_controller.o_status.config(text="Analysiere URL...", fg="blue")
                s_text = f"Titel {i}/{i_titels}: ..."
                self.main_controller.o_titel.config(text=s_text, fg="orange")
                b_valid_url = False
                try:
                    o_youtube = pytube.YouTube(s_url, on_progress_callback=self.progress_callback)
                    s_titel = o_youtube.title[:35]
                    s_text = f"Titel {i}/{i_titels}: {s_titel}"
                    self.main_controller.o_titel.config(text=s_text, fg="orange")
                    b_valid_url = True
                except BaseException:  # pylint: disable=bare-except
                    self.main_controller.o_status.config(text="Ungültige URL!", fg="red")
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
                        o_stream = None  # TODO
                        self.main_controller.o_status.config(text="Unerwarteter Fehler!", fg="red")
                    try:
                        self.main_controller.o_status.config(text="Download läuft...", fg="blue")
                        o_stream.download(S_DOWNLOAD_FOLDER + s_subfolder_name, s_filename)
                        self.main_controller.o_status.config(text="Download abgeschlossen!", fg="green")
                        if B_MP3_CONVERT:
                            if i_choice == 3:
                                self.main_controller.o_status.config(text="MP3 wird erstellt...", fg="blue")
                                s_file_path_name = S_DOWNLOAD_FOLDER + s_subfolder_name + "/" + o_stream.default_filename
                                audioclip = AudioFileClip(s_file_path_name)
                                audioclip.write_audiofile(s_file_path_name[:-1] + "3")
                                audioclip.close()
                                os.remove(s_file_path_name)
                                self.main_controller.o_status.config(text="MP3 erstellt!", fg="green")
                    except BaseException:  # pylint: disable=bare-except
                        self.main_controller.o_status.config(text="Dieses Video kann nicht heruntergeladen werden!",
                                                             fg="red")
        else:
            self.main_controller.o_status.config(text="Bitte Format angeben!", fg="red")
        self.main_controller.o_download_button["state"] = "normal"

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
                self.main_controller.o_status.config(text=f'Download läuft... noch {i_remaining_seconds}sek', fg="blue")
            self.f_time_stamp = f_actual_time
            self.i_last_bytes_remaining = bytes_remaining
            i_percent = int(((self.i_file_size - bytes_remaining) / self.i_file_size) * 100)
            i_percent_diff = i_percent - self.i_last_percent
            for _ in range(i_percent_diff):
                self.main_controller.o_progress.step()
            self.main_controller.style.configure('text.Horizontal.TProgressbar', text=f'{i_percent}%')
            self.i_last_percent = i_percent


if __name__ == "__main__":
    s_url = "https://www.youtube.com/watch?v=CE70PHlgrlo"
    try:
        o_youtube = pytube.YouTube(s_url)
    except BaseException:  # pylint: disable=bare-except
        print("Ungültige URL!")
    else:
        s_filename = None
        o_stream = o_youtube.streams.filter(only_audio=True).first()
        try:
            print("Download läuft...")
            o_stream.download(S_DOWNLOAD_FOLDER, s_filename)
            print("Download abgeschlossen!")
        except BaseException:  # pylint: disable=bare-except
            print("Dieses Video kann nicht heruntergeladen werden!")
