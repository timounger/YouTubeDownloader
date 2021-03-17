#!/usr/bin/env python3
# encoding: utf-8
"""
*****************************************************************************
 @file    youtube_downloader.py
 @brief   YouTube content download
*****************************************************************************
"""

from tkinter import *
from tkinter import ttk
import os
import subprocess
import pytube

S_VERSION = "0.1"
S_DEVELOPER_LABLE = "Timo Unger © 2021"

S_TITEL = "YouTube Downloader"
S_DOWNLOAD_FOLDER = "Download"

def download():
    """ download YouTube content"""
    choice = o_format.get()
    url = s_url.get()
    if len(url) > 1:
        s_status.config(text="")
        youtube_obj = pytube.YouTube(url)
        if choice == l_format[0]:
            select = youtube_obj.streams.filter(progressive=True).first()
        elif choice == l_format[1]:
            select = youtube_obj.streams.filter(progressive=True,file_extension='mp4').last()
        elif choice == l_format[2]:
            select = youtube_obj.streams.filter(only_audio=True).first()
        else:
            s_status.config(text="Bitte Format angeben!",fg="red")
    select.download(S_DOWNLOAD_FOLDER)
    s_status.config(text="Download abgeschlossen!", fg="green")

def open_download_folder():
    """ open download folder and create if not exist """
    if not os.path.isdir(S_DOWNLOAD_FOLDER):
        os.makedirs(S_DOWNLOAD_FOLDER)
    subprocess.Popen('explorer ' + S_DOWNLOAD_FOLDER)

if __name__ == "__main__":
    root = Tk()
    root.title(S_TITEL + " V%s\n" % S_VERSION)
    root.geometry("350x250") #set window
    root.columnconfigure(0,weight=1)#set all content in center.

    #YouTube Link Label
    ytdLabel = Label(root,text="Gebe die YouTube URL ein:",font=("jost",15))
    ytdLabel.grid()

    #Entry Box
    ytdEntryVar = StringVar()
    s_url = Entry(root,width=50,textvariable=ytdEntryVar)
    s_url.grid()

    #Error Message
    s_status = Label(root,text="Status",fg="red",font=("jost",10))
    s_status.grid()

    #Download Quality
    ytdQuality = Label(root,text="Wähle ein Format",font=("jost",15))
    ytdQuality.grid()

    l_format = ["720p","144p","Nur Audio"]
    o_format = ttk.Combobox(root,values=l_format)
    o_format.grid()

    #download button
    downloadbtn = Button(root,text="Download",width=10,bg="red",fg="white",command=download)
    downloadbtn.grid()

    #folder button
    downloadbtn = Button(root,text="Öffne Speicherort",width=15,bg="grey",fg="white",command=open_download_folder)
    downloadbtn.grid()

    #developer Label
    developerlabel = Label(root,text=S_DEVELOPER_LABLE,font=("Calibri",12))
    developerlabel.grid()
    root.mainloop()
