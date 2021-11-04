#!/usr/bin/env python3
# encoding: utf-8
"""
*****************************************************************************
 @file    youtube_api.py
 @brief   API to get links from playlist
          Code for YouTube API: "https://www.py4u.net/discuss/194200"
*****************************************************************************
"""

import sys
from urllib.parse import parse_qs, urlparse
import googleapiclient.discovery

S_API_KEY = "AIzaSyAeelVzvo3VUEsKCTJbC3Kvt4K8XJ46z_w" # API key for timounger92
S_YOUTUBE_URL = "https://www.youtube.com/watch?v="

def get_urls_of_playlist(s_url):
    """ get URLs of play list """
    query = parse_qs(urlparse(s_url).query, keep_blank_values=True)
    playlist_id = query["list"][0]
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = S_API_KEY)
    request = youtube.playlistItems().list(part = "snippet", playlistId = playlist_id, maxResults = 3)
    response = request.execute()
    l_urls = []
    while request is not None:
        response = request.execute()
        l_urls.append(S_YOUTUBE_URL + response["items"][0]["snippet"]["resourceId"]["videoId"])
        request = youtube.playlistItems().list_next(request, response)
    return l_urls

if __name__ == "__main__":
    S_PLAYLIST_URL = "https://www.youtube.com/watch?v=e3qLmEfjXfs&list=PL0MipQPbTie7KQujisznV6n-NGuv8aG-g"
    l_play_list = get_urls_of_playlist(S_PLAYLIST_URL)
    print("URL Count: %d" % len(l_play_list))
    print(l_play_list)
    sys.exit("END")
