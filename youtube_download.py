#!/usr/bin/env python3
# encoding: utf-8
"""
*****************************************************************************
 @file    youtube_download.py
 @brief   analysis and download content from YouTube URL
*****************************************************************************
"""

import sys
import os
import subprocess
import time
import re
import pytube
import threading
from moviepy.editor import AudioFileClip

S_DEBUG = False

S_DOWNLOAD_FOLDER = "Download"

L_FORMAT = [
    ("Hohe Auflösung",1),
    ("Niedrige Auflösung",2),
    ("Nur Audio",3)
]

class EState():
    ANALYSED = "Analyzed"
    QUEUED = "Queued"
    DOWNLOAD = "Download"
    FINISH = "Finish"

S_VIDEO_URL = "https://www.youtube.com/watch?v=%d" # q5WdWSpz1vQ
        
def progress_callback(self, _stream, _chunk, bytes_remaining):
    """ calculate process and update process bar """
    pass

class CAnalyzeUrl(threading.Thread):
    """ thread class for download """
    def __init__(self, l_queue, s_input, s_format):
        self.l_queue = l_queue
        self.s_input = s_input
        self.s_format = s_format
        threading.Thread.__init__(self)
    def run(self):
        """ analysis URL """
        s_input = self.s_input.splitlines()
        for s_url_text in s_input:
            l_url = []
            s_subfolder_name = None
            if re.search("&list=", s_url_text):
                o_playlist = pytube.Playlist(s_url_text)
                s_subfolder_name = o_playlist.title
                for video in o_playlist.videos:
                    l_url.append(video.watch_url)
            else:
                l_url = [s_url_text]
            for s_url in l_url:
                try:
                    o_youtube = pytube.YouTube(s_url)
                    s_titel = o_youtube.title
                    s_length = time.strftime("%H:%M:%S", time.gmtime(o_youtube.length))
                    s_id = o_youtube.video_id
                    l_entry = [s_titel, s_length, self.s_format, EState.ANALYSED, s_id, s_subfolder_name, o_youtube]
                    self.l_queue.append(l_entry)
                except: # pylint: disable=bare-except
                    pass

class CDownload(threading.Thread):
    """ thread class for download """
    def __init__(self, entry):
        threading.Thread.__init__(self)
        self.entry = entry
    def run(self):
        o_stream = self.entry[6].streams.filter(progressive=True, file_extension='mp4')\
                                             .get_highest_resolution()
        o_stream.download(S_DOWNLOAD_FOLDER)
        self.entry[3] = EState.FINISH
        sys.exit()

def open_download_folder():
    """ open download folder and create if not exist """
    if not os.path.isdir(S_DOWNLOAD_FOLDER):
        os.makedirs(S_DOWNLOAD_FOLDER)
    with subprocess.Popen('explorer ' + S_DOWNLOAD_FOLDER):
        pass

if __name__ == "__main__":
    sys.exit("END")