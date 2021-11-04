#!/usr/bin/env python3
# encoding: utf-8
"""
*****************************************************************************
 @file    youtube_html.py
 @brief   get playlist links from HTML
          Code for YouTube URL: "https://stackoverflow.com/questions/63192583/get-youtube-playlist-urls-with-python"
*****************************************************************************
"""

import sys
import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from webdriver_manager.firefox import GeckoDriverManager

S_YOUTUBE_URL = "https://www.youtube.com/watch?v="
S_VIDEO_START = "watch?v="

def get_urls_of_playlist(s_url):
    """ get URLs of play list """
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.minimize_window()
    driver.get(s_url)
    time.sleep(5)
    soup = bs(driver.page_source,'html.parser')
    driver.quit()
    res = soup.find_all('ytd-playlist-panel-video-renderer')
    l_urls = []
    if len(res) > 0:
        urls = re.findall('watch.*list', str(res))
        for s_url in urls:
            i_curser_pos = s_url.index(S_VIDEO_START) + len(S_VIDEO_START)
            i_curser_pos_end = i_curser_pos + 11
            l_urls.append(S_YOUTUBE_URL + s_url[i_curser_pos : i_curser_pos_end])
    l_urls = list(dict.fromkeys(l_urls)) # delete double entries
    return l_urls

if __name__ == "__main__":
    S_PLAYLIST_URL = "https://www.youtube.com/watch?v=e3qLmEfjXfs&list=PL0MipQPbTie7KQujisznV6n-NGuv8aG-g"
    l_play_list = get_urls_of_playlist(S_PLAYLIST_URL)
    print("URL Count: %d" % len(l_play_list))
    print(l_play_list)
    sys.exit("END")
