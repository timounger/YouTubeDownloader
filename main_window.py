#!/usr/bin/env python3
# encoding: utf-8
"""
*****************************************************************************
 @file    main_window.py
 @brief   main window for YouTubeDownloader
*****************************************************************************
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QIcon
from pyuic5.window import Ui_MainWindow
import threading
import time
import clipboard
import youtube_download as yd

L_ROW_DESCRIPTION = ["Titel", "Length", "Format", "Status", "ID"]

class CGui(object):
    def __init__(self, window, gui):
        self.gui = gui
        self.window = window
        window.setWindowTitle("YouTube Downloader")
        window.setWindowIcon(QIcon('app.ico'))
        gui.button_paste.clicked.connect(self.paste_clicked)
        gui.button_add.clicked.connect(self.add_clicked)
        gui.button_folder.clicked.connect(yd.open_download_folder)
        gui.button_download.clicked.connect(self.download_clicked)
        gui.table_queue.setRowCount(0)
        gui.table_queue.setColumnCount(len(L_ROW_DESCRIPTION))
        for i, value in enumerate(L_ROW_DESCRIPTION):
            item = QTableWidgetItem()
            gui.table_queue.setHorizontalHeaderItem(i, item)
            gui.table_queue.horizontalHeaderItem(i).setText(value)
        self.c_queue = CQueue(gui)
        self.c_queue.start()
        self.gui.text_url.setPlainText("https://www.youtube.com/watch?v=q5WdWSpz1vQ")
        self.gui.text_url.setPlainText("https://www.youtube.com/watch?v=K6lThwljr2M&list=PL9HJJedWjAmNILSM93NSf0-5-VoLXs_6Q&index=2")
    def add_clicked(self):
        self.gui.statusbar.showMessage("URL wird analysiert...")
        s_input = self.gui.text_url.toPlainText()
        s_format = self.gui.combo_format.currentText()
        self.gui.text_url.clear()
        self.c_queue.l_queue += yd.analysis_url(s_input, s_format)
        self.gui.statusbar.showMessage("URL wurde analysiert!")
    def paste_clicked(self):
        """ input text from clipboard to entry box """
        self.gui.text_url.setPlainText(clipboard.paste())
        self.gui.statusbar.showMessage("Text aus Zwischenablage wurde eingefügt!")
    def download_clicked(self):
        self.gui.statusbar.showMessage("Videos werden heruntergeladen...")

class CQueue(threading.Thread):
    """ thread class for queue """
    def __init__(self, gui):
        threading.Thread.__init__(self)
        self.gui = gui
        self.l_queue = []
    def run(self):
        time.sleep(0.001)
        while True:
            time.sleep(0.1)
            self.set_status_table()
    def set_status_table(self):
        pass
        """
        table = self.gui.table_queue
        row_cnt = table.rowCount()
        i_id_pos = 4
        i_format_pos = 2
        b_removed = False
        for i_row in range(0, row_cnt):
            b_exist = False
            for entry in self.l_queue:
                if (table.item(i_row, i_id_pos).text() == entry[i_id_pos])\
                   and (table.item(i_row, i_format_pos).text() == entry[i_format_pos]):
                    b_exist = True
                    break
            if not b_exist:
                table.removeRow(i_row)
                b_removed = True
                break
        if not b_removed:
            for entry in self.l_queue:
                b_entry_exist = False
                row_cnt = table.rowCount()
                i_update_pos = row_cnt
                for i_row in range(0, row_cnt):
                    if (table.item(i_row, i_id_pos).text() == entry[i_id_pos])\
                       and (table.item(i_row, i_format_pos).text() == entry[i_format_pos]):
                        b_entry_exist = True
                        i_update_pos = i_row
                        break
                if not b_entry_exist:
                    table.insertRow(row_cnt)
                for i, _ in enumerate(L_ROW_DESCRIPTION):
                    table.setItem(i_update_pos, i, QTableWidgetItem(entry[i]))
    """
if __name__ == "__main__":
    o_app = QApplication(sys.argv)
    o_window = QMainWindow()
    ui_window = Ui_MainWindow()
    ui_window.setupUi(o_window)
    c_gui = CGui(o_window, ui_window)
    o_window.show()
    sys.exit(o_app.exec_())
