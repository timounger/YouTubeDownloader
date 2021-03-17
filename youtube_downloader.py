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

l_format = [
    ("720p",1),
    ("144p",2),
    ("Nur Audio",3)
]

def download():
    """ download YouTube content"""
    i_choice = o_format_choice.get()
    s_url = o_url_choice.get()
    if  i_choice != 0:
        b_valid_url = False
        try:
            youtube_obj = pytube.YouTube(s_url)
            b_valid_url = True
        except:
            o_status.config(text="Ungültige URL!",fg="red")
        if b_valid_url:
            if i_choice == 1:
                select = youtube_obj.streams.filter(progressive=True).first()
            elif i_choice == 2:
                select = youtube_obj.streams.filter(progressive=True,file_extension='mp4').last()
            elif i_choice == 3:
                select = youtube_obj.streams.filter(only_audio=True).first()
            else:
                select = youtube_obj.streams.filter(progressive=True).first()
            select.download(S_DOWNLOAD_FOLDER)
            o_status.config(text="Download abgeschlossen!", fg="green")
    else:
        o_status.config(text="Bitte Format angeben!",fg="red")

def open_download_folder():
    """ open download folder and create if not exist """
    if not os.path.isdir(S_DOWNLOAD_FOLDER):
        os.makedirs(S_DOWNLOAD_FOLDER)
    subprocess.Popen('explorer ' + S_DOWNLOAD_FOLDER)

if __name__ == "__main__":
    root = Tk()
    root.title(S_TITEL + " V%s\n" % S_VERSION)
    root.geometry("350x250") #set window
    root.columnconfigure(0,weight=1) #set all content in center.

    #YouTube Link Label
    ytdLabel = Label(root,text="Gebe die YouTube URL ein:",font=("jost",15))
    ytdLabel.grid()

    #Entry Box
    o_url_choice = StringVar()
    o_url = Entry(root,width=50,textvariable=o_url_choice)
    o_url.grid()

    #Error Message
    o_status = Label(root,text="Status",fg="red",font=("jost",10))
    o_status.grid()

    # format label
    o_format_label = Label(root,text="Wähle ein Format",font=("jost",15))
    o_format_label.grid()
    
    # format radio button
    o_format_choice = IntVar()
    for txt, val in l_format:
        o_format = Radiobutton(root, text=txt, padx = 20, variable = o_format_choice, value=val)
        o_format.grid()

    #download button
    o_download_button = Button(root,text="Download",width=10,bg="red",fg="white",command=download)
    o_download_button.grid()

    #folder button
    o_download_button = Button(root,text="Öffne Speicherort",width=15,bg="grey",fg="white",command=open_download_folder)
    o_download_button.grid()

    #developer Label
    o_developer_label = Label(root,text=S_DEVELOPER_LABLE,font=("Calibri",12))
    o_developer_label.grid()
    root.mainloop()
