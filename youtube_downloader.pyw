#!/usr/bin/env python3
# encoding: utf-8
"""
*****************************************************************************
 @file    youtube_downloader.pyw
 @brief   YouTube content download
*****************************************************************************
"""

import os
import base64
from tkinter import Label, Tk, StringVar, IntVar, Entry, Radiobutton, Button, Menu
from tkinter.ttk import Progressbar, Style
import statistics
import subprocess
import threading
import time
import clipboard
import pytube

S_VERSION = "0.3"
S_DEVELOPER_LABLE = "Timo Unger © 2021"

S_TITEL = "YouTube Downloader"
S_DOWNLOAD_FOLDER = "Download"

I_SPEED_AVERAGE_VALUES = 10

L_FORMAT = [
    ("Hohe Auflösung",1),
    ("Niedrige Auflösung",2),
    ("Nur Audio",3)
]

S_ICON = """
AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAACUWAAAlFgAAAAAAAAAAAAArMcj/KzHI/ysxyP8rMcj\
/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/yAmxf9QVdH/ICbF/ykwx/8rMcj/KzHI/ysxyP8rMcj/KzHI/y\
sxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rM\
cj/KzHI/ysxyP8jKcb/MjjJ///////Exe//DBLA/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI\
/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/Ji3G/yEnxf////////////////+\
XmuP/ExrC/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/Kz\
HI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ykvx/8SGMH/7e36//////////////////////9ladb/GyLE/ysxyP8rMcj/KzHI/ysxy\
P8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8qMMf/\
DRTA/8zO8f////////////////////////////////9ARc3/ISfF/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ys\
xyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/xEXwf+kp+f///////////////////////////////\
////////////8oL8f/JizG/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/\
ysxyP8rMcj/KzHI/ysxyP8XHsL/eX3c//////////////////////////////////////////////////X2/P8SGcH/KS/H/ysxyP8r\
Mcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/ICbF/1ld1P/////////\
//////////////////////////////////////////////////9zd9f8OFcD/KjDH/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP\
8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ycux/86P8v///////f3/P/y8vv//////////////////////////////////\
/////b2/P/09fz//////6Wo5/8eJMT/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysx\
yP8rMcj/KzHI/yctx/8UGsH/ExrB/wAAuv/v8Pv/////////////////////////////////RUrP/wwSv/8TGcH/HSTE/ysxyP8rMcj\
/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/ERjA//\
Pz+/////////////////////////////////9WXNP/JCrG/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rM\
cj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8RGMD/8/P8////////////////////////////////\
/1Zc0/8kKsb/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8\
rMcj/KzHI/ysxyP8rMcj/KzHI/xEYwP/z8/z/////////////////////////////////VlzT/yQqxv8rMcj/KzHI/ysxyP8rMcj/Kz\
HI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/ERjA//Pz/\
P////////////////////////////////9WXNP/JCrG/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/\
KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8RGMD/8/P8/////////////////////////////////1Z\
c0/8kKsb/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMc\
j/KzHI/ysxyP8rMcj/KzHI/xEYwP/y8/z/////////////////////////////////VlzT/yQqxv8rMcj/KzHI/ysxyP8rMcj/KzHI/\
ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/ERjA////////\
//////////////////////////////9cYdX/IyrG/yowyP8qMMj/KjDI/yowyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzH\
I/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8nLcb/OkDL/zo/y/80Ocr/LjTI/y0zyP8sMcf/LjTI/x4kxP\
8aIMP/GyHD/xshw/8bIcP/GyLE/xwixP8dI8T/HiTE/x8lxf8jKcb/KjDH/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/K\
zHI/ysxyP8rMcj/KzHI/ysxyP8nLcf/Fx7D/0dMz/9+gt3/i47h/5eZ4/+foub/qazo/62w6f+tsOn/rbDp/62v6f+qrOj/pKfn/5ue\
5P+SleL/honf/15j1f8YHsP/KjDH/ysxyP8rMcj/IynG/ygux/8rMcj/JizG/yEoxf8pL8f/KjDH/yEoxf8mLMb/IyrG/yEoxf9pbtf\
//////////////////////////////////////////////////////////////////////////////////////5qd5P8cI8T/KzHI/y\
Mpxv9qbtj/O0DL/yAmxf89Qsz/fIDc/x0jxP8gJsX/eX3c/zc8y/9kadb/DRTA/+jo+f///////Pz+/9LT8////////f7+/9HS8v/19\
fz/6+v5/+zs+v/y8/v/ysvx////////////4eL3/8/R8v///////////xQawf8rMcj/EhnB//////9ydtr/Jy3G////////////z9Dy\
/0VKzv////////////////8ABbz////////////m5/j/AAC2//////+Qk+H/IynG/ygux/+LjuH/lJji/yMpxf8YHsP/jZHh/9TW9P8\
TGcH/HyXE/5ea4///////LjPI/ysxyP8TGcH//////2ds1/9ZXtP//////ykvx///////RUrO//7+/v9DSM7//////wgPvv////////\
///+zt+f8AA7v//////4WI3/+Pk+H/l5rj/46R4f+Ym+P/f4Pd/5mb5P97f93/i47g/5SX4//Q0fP/dXna//////9BR83/KzHI/w8Ww\
f//////Y2jW/1hd0///////MznJ//////9GS8///v7+/0xR0P////7/DxbA////////////6+v5/wACu///////hIjf/4iM4P+SleL/\
jpHh/5ib4/93fNv/kJPh/3yA3f+Ul+L/QkjO/5GU4v++wO7//////05T0P8oLsf/ISjF//////+NkOH/VFjS//////8qMMf//////0Z\
Lz//8/P7/TFHQ/////v8TGsH////////////p6vn/AAK7//////+Eh9//io3g/5KU4v+OkeH/mJvj/3yA3P+TluP/fIDd/5GU4v9gZd\
X/cnba/1Va0v//////T1TQ/yAnxf93e9v//////+Xm+P80Ocr//////5SX4///////Sk/Q//////9OU9H//////w8WwP///////////\
+jp+f8AArv//////36C3v+FiN//i4/g/4iL4P+dn+T/Sk/Q/1le0/98f93/oaPm/1RZ0v90eNr/bnPZ//////9PVNH/FRvC/9zc9f+h\
pOb//////x0jxP+cn+X/8PH7/05S0P9MUND/wMLu/0RJzv/IyfD/DxbA////////////8fP7/wACu///////trjs/7a47P+6vO3/vb/\
t/5WY4v9na9f/X2PV/93e9v//////cHTZ/2Bk1f///////////0BGzf8eJMT//////zg/y//5+f3/io7g/xIYwf8WHcL/JCrG/yUrxv\
8bIcP/JSvG/xohw/8VHML//////9LT8/97f9z/CA+//5CT4f/r7Pn/////////////////hIfe/3Z62////////////////////////\
///////////////KzHI/1NY0f/g4fb/EhnB/4yP4P+nquf/HiTE/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/xUbwv/u7vr/wMLu/19j\
1f90eNr/XGHU/9na9f////////////////+vsur/pafn//////////////////////////////////////8UGsH/JSvG/xgfw/8qMMf\
/HybF/x4kxP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/IijF/2Nn1v////////////////////////////////////////////\
//////////////////////////////////////////lZjj/x0jxP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rM\
cj/KzHI/ysxyP8rMcj/HCLE/0dMz/99gN3/h4vf/5SX4v+doOX/oaTm/6Kl5v+ipOb/oqTm/6Kk5v+ipOb/nqHl/5WX4/+Ii+D/f4Pd\
/1hd0/8YHsL/KjDH/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/KzHI/ysxyP8rMcj/JSvG/yAmxf8\
fJcT/HSTE/xwjxP8cIsT/HCLE/xwixP8cIsT/HCLE/xwixP8cI8T/HSTE/x4lxP8gJsX/JCrG/yowx/8rMcj/AAAAAAAAAAAAAAAAAA\
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=
"""

# global variables
c_gui = []

class CdownloadThread(threading.Thread):
    """ thread class for download """
    def __init__(self):
        threading.Thread.__init__(self)
        self.b_first_callback_call = False
        self.i_file_size = 0
        self.i_last_persent = 0
        self.f_time_stamp = 0.0
        self.i_last_bytes_remaining = 0
        self.d_speed_history = [] # download speed history
    def run(self):
        """ download YouTube content"""
        c_gui.o_status.config(text="Analysiere URL...", fg="blue")
        i_choice = c_gui.o_format_choice.get()
        s_url = c_gui.o_url_choice.get()
        if  i_choice != 0:
            b_valid_url = False
            try:
                o_youtube = pytube.YouTube(s_url, on_progress_callback=self.progress_callback)
                b_valid_url = True
            except: # pylint: disable=bare-except
                c_gui.o_status.config(text="Ungültige URL!",fg="red")
            if b_valid_url:
                if i_choice == 1:
                    o_stream = o_youtube.streams.filter(progressive=True, file_extension='mp4')\
                                                         .get_highest_resolution()
                elif i_choice == 2:
                    o_stream = o_youtube.streams.filter(progressive=True, file_extension='mp4')\
                                                         .get_lowest_resolution()
                elif i_choice == 3:
                    o_stream = o_youtube.streams.filter(only_audio=True).first()
                else:
                    c_gui.o_status.config(text="Unerwarteter Fehler!",fg="red")
                try:
                    c_gui.o_status.config(text="Download läuft...", fg="blue")
                    o_stream.download(S_DOWNLOAD_FOLDER)
                    c_gui.o_status.config(text="Download abgeschlossen!", fg="green")
                except: # pylint: disable=bare-except
                    c_gui.o_status.config(text="Dieses Video kann nicht heruntergeladen werden!",\
                                          fg="red")
        else:
            c_gui.o_status.config(text="Bitte Format angeben!",fg="red")
    def progress_callback(self, _stream, _chunk, bytes_remaining):
        """ calculate process and update process bar"""
        if not self.b_first_callback_call:
            self.i_file_size = bytes_remaining
            self.i_last_bytes_remaining = bytes_remaining
            self.b_first_callback_call = True
        else:
            f_actual_time = time.time()
            if (f_actual_time - self.f_time_stamp) > 1:  # 1 second is over
                if self.f_time_stamp != 0: # set calculate time only for second call
                    i_actual_speed = (self.i_last_bytes_remaining - bytes_remaining)
                    i_history_len = len(self.d_speed_history)
                    if i_history_len < I_SPEED_AVERAGE_VALUES:
                        self.d_speed_history.append(i_actual_speed)
                    else:
                        for i, value in enumerate(self.d_speed_history):
                            if i != 0:
                                self.d_speed_history[i-1] = value
                        self.d_speed_history[I_SPEED_AVERAGE_VALUES-1] = i_actual_speed
                    i_average_speed = statistics.mean(self.d_speed_history)
                    i_remaining_seconds = int(bytes_remaining / i_average_speed)
                    c_gui.o_status.config(text="Download läuft... noch %dsek"\
                                          % i_remaining_seconds, fg="blue")
                self.f_time_stamp = f_actual_time
                self.i_last_bytes_remaining = bytes_remaining
        i_percent = int(((self.i_file_size - bytes_remaining) / self.i_file_size) * 100)
        if self.i_last_persent != i_percent: # one percent is over then step process bar
            c_gui.o_progress.step()
            c_gui.style.configure('text.Horizontal.TProgressbar', text='%d%%' % i_percent)
            self.i_last_persent = i_percent

class CyoutubeDownloadGui:
    """ class for YouTube download GUI """
    def __init__(self): # pylint: disable=R0914
        self.root = Tk()
        self.root.title(S_TITEL + " V%s\n" % S_VERSION)
        icondata = base64.b64decode(S_ICON) # The Base64 icon version as a string
        s_temp_file= "temp_icon.ico" # The temporary file
        iconfile= open(s_temp_file,"wb")
        iconfile.write(icondata) # Extract the icon
        iconfile.close()
        self.root.wm_iconbitmap(s_temp_file) # set icon
        os.remove(s_temp_file) # Delete the tempfile
        self.root.geometry("350x300") #set window
        self.root.resizable(0, 0) # Don't allow resizing
        self.root.columnconfigure(0,weight=1) #set all content in center.
        self.o_url_choice = StringVar()
        self.o_format_choice = IntVar()
        #YouTube Link Label
        o_url_label = Label(self.root,text="Gebe die YouTube URL ein:",font=("jost",15))
        o_url_label.grid()
        #Entry Box
        self.o_url = Entry(self.root,width=50,textvariable=self.o_url_choice)
        self.o_url.bind("<Button-3>", self.do_popup) # event for right mouse click (button 3)
        s_clipboard_text = clipboard.paste() # get content of clip board
        s_compare_string = "https://"
        b_valid_url = False
        if     (len(s_clipboard_text) < 50)\
           and (s_clipboard_text[0:len(s_compare_string)] == s_compare_string):
            try:
                pytube.YouTube(s_clipboard_text)
                b_valid_url = True
            except: # pylint: disable=bare-except
                b_valid_url = False
        if b_valid_url:
            s_default_text = s_clipboard_text
            s_default_status = "URL aus Zwischenablage wurde eingefügt!"
        else:
            s_default_text = "" # if no YouTube link or invalid set no text as default
            s_default_status = "URL eingeben und Downlaod starten!"
        self.o_url.insert(0, s_default_text) # set content of clipboard as default
        self.o_url.grid()
        o_input_button = Button(self.root,text="Einfügen",width=10,\
                                bg="green",fg="white",command=self.input_link)
        o_input_button.grid()
        #Error Message
        self.o_status = Label(self.root,text=s_default_status,fg="blue",font=("jost",10))
        self.o_status.grid()
        # progress bar
        self.style = Style(self.root)
        self.style.layout('text.Horizontal.TProgressbar',
                     [('Horizontal.Progressbar.trough',
                       {'children': [('Horizontal.Progressbar.pbar',
                                      {'side': 'left', 'sticky': 'ns'})],
                        'sticky': 'nswe'}),
                      ('Horizontal.Progressbar.label', {'sticky': ''})])
        self.style.configure('text.Horizontal.TProgressbar', text='0 %')
        self.o_progress = Progressbar(self.root,style='text.Horizontal.TProgressbar',\
                                      length=200,  maximum=100, value=0,)
        self.o_progress.grid()
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
                                   bg="red",fg="white",command=self.start_download)
        o_download_button.grid()
        #folder button
        o_download_button = Button(self.root,text="Öffne Speicherort",width=15,\
                                   bg="grey",fg="white",command=self.open_download_folder)
        o_download_button.grid()
        #developer Label
        o_developer_label = Label(self.root,text=S_DEVELOPER_LABLE,font=("Calibri",12))
        o_developer_label.grid()
        # right click content menu
        self.menu = Menu(self.root, tearoff = 0)
        self.menu.add_command(label ="Ausschneiden", command=self.cut)
        self.menu.add_command(label ="Kopieren", command=self.copy)
        self.menu.add_command(label ="Einfügen", command=self.paste)
    def copy(self):
        """ copy selected text to clipboard """
        copy_selected_text_to_clipboard(self.o_url)
    def cut(self):
        """ copy selected text to clipboard and cut text out """
        copy_selected_text_to_clipboard(self.o_url)
        delete_selected_text(self.o_url)
    def paste(self):
        """ paste text from clipboard to position """
        delete_selected_text(self.o_url)
        self.o_url.insert(self.o_url.index('insert'), clipboard.paste()) # paste at cursor position
    def do_popup(self, event):
        """ pop up content menu """
        try:
            self.o_url.selection_get()
            self.menu.entryconfig("Kopieren", state="normal")
            self.menu.entryconfig("Ausschneiden", state="normal")
        except: # pylint: disable=bare-except
            self.menu.entryconfig("Kopieren", state="disabled")
            self.menu.entryconfig("Ausschneiden", state="disabled")
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()
    def input_link(self):
        """ input texyt from clipboard to entry box """
        self.o_url.delete(0, "end")
        self.o_url.insert(0, clipboard.paste()) # paste content of clipboard
        self.o_status.config(text="Text aus Zwischenablage wurde eingefügt!",fg="blue")
    def start_download(self): # pylint: disable=R0201
        """ create and start thread for download """
        c_download = CdownloadThread()
        c_download.start()
    def open_download_folder(self): # pylint: disable=R0201
        """ open download folder and create if not exist """
        if not os.path.isdir(S_DOWNLOAD_FOLDER):
            os.makedirs(S_DOWNLOAD_FOLDER)
        subprocess.Popen('explorer ' + S_DOWNLOAD_FOLDER)

def copy_selected_text_to_clipboard(o_url):
    """ copy selected text to clipboard """
    s_text = o_url.selection_get()
    clipboard.copy(s_text)

def delete_selected_text(o_url):
    """ delete selected text from URL """
    try:
        s_select_text = o_url.selection_get()
    except: # pylint: disable=bare-except
        pass
    else:
        s_enty_text = o_url.get()
        i_selected_text_length = len(s_select_text)
        i_curser_pos = o_url.index('insert')
        i_curser_pos_end = i_curser_pos + i_selected_text_length
        s_text_to_check = s_enty_text[i_curser_pos : i_curser_pos_end]
        if s_text_to_check == s_select_text:
            o_url.delete(i_curser_pos, i_curser_pos_end)
        else:
            o_url.delete(i_curser_pos - i_selected_text_length, i_curser_pos)

if __name__ == "__main__":
    c_gui = CyoutubeDownloadGui()
    c_gui.root.mainloop()
