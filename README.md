\mainpage YouTubeDownloader

\tableofcontents

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/timounger/YouTubeDownloader)](https://github.com/timounger/YouTubeDownloader/releases/latest)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-red.svg)](https://github.com/timounger/YouTubeDownloader/blob/master/LICENSE.md)
[![Python version](https://img.shields.io/badge/python-3.11.9-blue)](https://www.python.org/downloads/release/python-3119/)
[![Code style: autopep8](https://img.shields.io/badge/code%20style-autopep8-green.svg)](https://github.com/hhatto/autopep8)
![GitHub Repo stars](https://img.shields.io/github/stars/timounger/YouTubeDownloader)

## Über ℹ️

Das YouTube Downloader Tool läd Inhalte von YouTube herunter.

![YouTubeDownloader](Documentation/img/app.png)

## Download ☁️ ⬇️

Die freigegebenen Versionen sind auf GitHub veröffentlicht und können dort [heruntergeladen](https://github.com/timounger/YouTubeDownloader/releases/latest) werden.

## Bug Fix

```py
    # Fix: https://github.com/pytube/pytube/issues/1954#issuecomment-2218287594
    # Change the function_patterns array in cipher.py at line 264 to include this one and it seems to work:

    function_patterns = [
    # https://github.com/ytdl-org/youtube-dl/issues/29326#issuecomment-865985377
    # https://github.com/yt-dlp/yt-dlp/commit/48416bc4a8f1d5ff07d5977659cb8ece7640dcd8
    # var Bpa = [iha];
    # ...
    # a.C && (b = a.get("n")) && (b = Bpa[0](b), a.set("n", b),
    # Bpa.length || iha("")) }};
    # In the above case, `iha` is the relevant function name
    r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&.*?\|\|\s*([a-z]+)',
    r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
    r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
    ]
```

## OS Support

Getestet mit

- Windows 11, Windows 10

## Credits

Besonderen Dank an alle Mitwirkenden:
<br><br>
<a href="https://github.com/timounger/YouTubeDownloader/graphs/contributors">
<img src="https://contrib.rocks/image?repo=timounger/YouTubeDownloader" />
</a>
