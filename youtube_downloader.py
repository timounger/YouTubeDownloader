#!/usr/bin/env python3
# encoding: utf-8
"""
*****************************************************************************
 @file    youtube_downloader.py
 @brief   YouTube content download_loop
*****************************************************************************
"""

from tkinter import *
from tkinter import ttk
import subprocess
import pytube

S_VERSION = "0.1"
S_TITEL = "YouTube Downloader"
S_DOWNLOAD_FOLDER = "Download"

def download():
    choice = o_format.get()
    url = s_url.get()
    if(len(url) > 1):
        s_status.config(text="")
        yt = pytube.YouTube(url)
        if(choice == choices[0]):
            select = yt.streams.filter(progressive=True).first()
        elif(choice == choices[1]):
            select = yt.streams.filter(progressive=True,file_extension='mp4').last()
        elif(choice == choices[2]):
            select = yt.streams.filter(only_audio=True).first()
        else:
            s_status.config(text="Bitte Format angeben!",fg="red")
    select.download(S_DOWNLOAD_FOLDER)
    s_status.config(text="Download abgeschlossen!")
    subprocess.Popen('explorer ' + S_DOWNLOAD_FOLDER)
root = Tk()
root.title(S_TITEL + " V%s\n" % S_VERSION)
root.geometry("350x180") #set window
root.columnconfigure(0,weight=1)#set all content in center.

#Ytd Link Label
ytdLabel = Label(root,text="Gebe die YouTube URL ein:",font=("jost",15))
ytdLabel.grid()

#Entry Box
ytdEntryVar = StringVar()
s_url = Entry(root,width=50,textvariable=ytdEntryVar)
s_url.grid()

#Error Msg
s_status = Label(root,text="Status",fg="red",font=("jost",10))
s_status.grid()

#Download Quality
ytdQuality = Label(root,text="Wähle ein Format",font=("jost",15))
ytdQuality.grid()

#combobox
choices = ["720p","144p","Nur Audio"]
o_format = ttk.Combobox(root,values=choices)
o_format.grid()

#download button
downloadbtn = Button(root,text="Download",width=10,bg="red",fg="white",command=download)
downloadbtn.grid()

#developer Label
developerlabel = Label(root,text="Timo Unger © 2021",font=("Calibri",12))
developerlabel.grid()
root.mainloop()
