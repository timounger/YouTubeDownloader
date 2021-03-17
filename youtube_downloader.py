#!/usr/bin/env python3
# encoding: utf-8
"""
*****************************************************************************
 @file    youtube_downloader.py
 @brief   YouTube content download
*****************************************************************************
"""

from tkinter import Label, Tk, StringVar, IntVar, Entry, Radiobutton, Button
import os
import subprocess
import pytube

S_VERSION = "0.1"
S_DEVELOPER_LABLE = "Timo Unger © 2021"

S_TITEL = "YouTube Downloader"
S_DOWNLOAD_FOLDER = "Download"

L_FORMAT = [
    ("720p",1),
    ("144p",2),
    ("Nur Audio",3)
]

# global variables
c_gui = []

class CyoutubeDownloadGui:
    """ class for YouTube download GUI """
    def __init__(self):
        self.root = Tk()
        self.root.title(S_TITEL + " V%s\n" % S_VERSION)
        #self.root.iconbitmap('Tool/app.ico')
        self.root.geometry("350x250") #set window
        self.root.columnconfigure(0,weight=1) #set all content in center.
        self.o_url_choice = StringVar()
        self.o_format_choice = IntVar()
        #YouTube Link Label
        o_url_label = Label(self.root,text="Gebe die YouTube URL ein:",font=("jost",15))
        o_url_label.grid()
        #Entry Box
        o_url = Entry(self.root,width=50,textvariable=self.o_url_choice)
        o_url.grid()
        #Error Message
        self.o_status = Label(self.root,text="Status",fg="red",font=("jost",10))
        self.o_status.grid()
        # format label
        o_format_label = Label(self.root,text="Wähle ein Format:",font=("jost",14))
        o_format_label.grid()
        # format radio button
        for txt, val in L_FORMAT:
            o_format = Radiobutton(self.root, text=txt, padx = 20,\
                                   variable = self.o_format_choice, value=val)
            o_format.grid()
        self.o_format_choice.set(1) # set first radio button as default
        #download button
        o_download_button = Button(self.root,text="Download",width=10,\
                                   bg="red",fg="white",command=self.download)
        o_download_button.grid()
        #folder button
        o_download_button = Button(self.root,text="Öffne Speicherort",width=15,\
                                   bg="grey",fg="white",command=self.open_download_folder)
        o_download_button.grid()
        #developer Label
        o_developer_label = Label(self.root,text=S_DEVELOPER_LABLE,font=("Calibri",12))
        o_developer_label.grid()
    def download(self):
        """ download YouTube content"""
        i_choice = self.o_format_choice.get()
        s_url = self.o_url_choice.get()
        if  i_choice != 0:
            b_valid_url = False
            try:
                youtube_obj = pytube.YouTube(s_url)
                b_valid_url = True
            except: # pylint: disable=bare-except
                self.o_status.config(text="Ungültige URL!",fg="red")
            if b_valid_url:
                if i_choice == 1:
                    o_stream = youtube_obj.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
                elif i_choice == 2:
                    o_stream = youtube_obj.streams.filter(progressive=True, file_extension='mp4').get_lowest_resolution()
                elif i_choice == 3:
                    o_stream = youtube_obj.streams.filter(only_audio=True).first()
                else:
                    self.o_status.config(text="Unerwarteter Fehler!",fg="red")
                #for stream in youtube_obj.streams.filter(progressive=True, file_extension='mp4'): print(stream)
                #print(o_stream)
                o_stream.download(S_DOWNLOAD_FOLDER)
                self.o_status.config(text="Download abgeschlossen!", fg="green")
        else:
            self.o_status.config(text="Bitte Format angeben!",fg="red")
    def open_download_folder(self): # pylint: disable=R0201
        """ open download folder and create if not exist """
        if not os.path.isdir(S_DOWNLOAD_FOLDER):
            os.makedirs(S_DOWNLOAD_FOLDER)
        subprocess.Popen('explorer ' + S_DOWNLOAD_FOLDER)

if __name__ == "__main__":
    c_gui = CyoutubeDownloadGui()
    c_gui.root.mainloop()
