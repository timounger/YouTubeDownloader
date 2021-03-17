#!/usr/bin/env python3
# encoding: utf-8
"""
*****************************************************************************
 @file    youtube_downloader.py
 @brief   YouTube content download_loop
*****************************************************************************
"""

import subprocess
import pytube
from tkinter import *

S_VERSION = "0.1"
S_TITEL = "YouTube Downloader"
S_DOWNLOAD_FOLDER = "Download"

b_button_mp4_pressed = False

def download():
    """ download YouTube content and open explorer if successful """
    notif.config(fg="green",text="Download wird durchgeführt...")
    try:
        yt_obj = pytube.YouTube(s_url.get())
        filters = yt_obj.streams.filter(progressive=True, file_extension="mp4")
        # download_loop the highest quality video
        filters.get_highest_resolution().download(S_DOWNLOAD_FOLDER)
        notif.config(fg="green",text="Download war erfolgreich!")
        subprocess.Popen('explorer ' + S_DOWNLOAD_FOLDER)
    except Exception: # pylint: disable=broad-except 
        notif.config(fg="red",text="Download war nicht erfolgreich!")

if __name__ == "__main__":
    master = Tk()
    master.title(S_TITEL + " V%s\n" % S_VERSION)
    Label(master, text=S_TITEL,fg="red",font=("Calibri",15)).grid(sticky=N,padx=100,row=0)
    Label(master,text="Gebe die YouTube URL ein:",font=("Calibri",12)).grid(sticky=N,row=1,pady=15)
    Label(master, text="Timo Unger © 2021",fg="black",font=("Calibri",12)).grid(sticky=N,padx=100,row=6)
    notif = Label(master,font=("Calibri",12))
    notif.grid(sticky=N,pady=1,row=5)
    s_url=StringVar()
    Entry(master,width=50,textvariable=s_url).grid(sticky=N,row=2)
    Button(master,width=20,text="Download .mp4",font=("Calibri",12),command=download).grid(sticky=N,row=3,pady=15) #Button mp4
    Button(master,width=20,text="Download .mp3",font=("Calibri",12),command=download).grid(sticky=N,row=4,pady=15) #Button mp3
    master.mainloop()
