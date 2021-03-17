#!/usr/bin/env python3
# encoding: utf-8
"""
*****************************************************************************
 @file    youtube_downloader.py
 @brief   YouTube content download_loop
*****************************************************************************
"""

import sys
import subprocess
import pytube

S_VERSION = "0.1"
S_DOWNLOAD_FOLDER = "Download"

def download(s_url, s_format):
    """ download YouTube content and open explorer if successful """
    try:
        print("Download wird durchgeführt...")
        yt_obj = pytube.YouTube(s_url)
        filters = yt_obj.streams.filter(progressive=True, file_extension="mp4")
        # download_loop the highest quality video
        filters.get_highest_resolution().download(S_DOWNLOAD_FOLDER)
        print('Download war erfolgreich!')
        subprocess.Popen('explorer ' + S_DOWNLOAD_FOLDER)
    except Exception as s_error: # pylint: disable=broad-except 
        print(s_error)
        print('Download war nicht erfolgreich!')

def user_input(s_text):
    print(s_text)
    s_input = input(">> ")
    return s_input

def download_loop():
    """ download loop for YouTube content """
    print("Youtube Downloader V%s\n" % S_VERSION)
    b_run = True
    while b_run:
        s_url = user_input("Gebe die YouTube URL ein:")
        """
        s_format_input = user_input("Drücke Enter für ein mp4 Format, gebe 0 ein für eine mp3:")
        if s_format_input == "0":
            s_format = "mp4"
        else:
            s_format = "mp3"
        """
        download(s_url, s_format)
        s_input = user_input("Drücke Enter um das Programm zu beenden, gebe 0 ein für einen weiteren Download.")
        if s_input == "0":
            b_run = True
        else:
            b_run = False

if __name__ == "__main__":
    download_loop()
    sys.exit("PROGRAM END")
