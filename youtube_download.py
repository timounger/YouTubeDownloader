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
from moviepy.editor import AudioFileClip

S_DEBUG = False

S_DOWNLOAD_FOLDER = "Download"

L_FORMAT = [
    ("Hohe Auflösung",1),
    ("Niedrige Auflösung",2),
    ("Nur Audio",3)
]

S_VIDEO_URL = "https://www.youtube.com/watch?v=%d" # q5WdWSpz1vQ
        
def progress_callback(self, _stream, _chunk, bytes_remaining):
    """ calculate process and update process bar """
    pass

def analysis_url(s_text, i_choice):
    """ analysis URL """
    l_video_list = []
    s_text = s_text.splitlines()
    for s_url_text in s_text:
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
                o_youtube = pytube.YouTube(s_url, on_progress_callback=progress_callback)
                s_titel = o_youtube.title
                s_length = time.strftime("%H:%M:%S", time.gmtime(o_youtube.length))
                s_id = o_youtube.video_id
                l_video_list.append([s_titel, s_length, i_choice, "Ready", s_id, s_subfolder_name, o_youtube])
            except: # pylint: disable=bare-except
                pass
    return l_video_list

def open_download_folder():
    """ open download folder and create if not exist """
    if not os.path.isdir(S_DOWNLOAD_FOLDER):
        os.makedirs(S_DOWNLOAD_FOLDER)
    with subprocess.Popen('explorer ' + S_DOWNLOAD_FOLDER):
        pass

if __name__ == "__main__":
    sys.exit("END")