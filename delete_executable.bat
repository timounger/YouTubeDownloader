:: "delete_youtube_downloader_executable.bat"
:: delete created files of YouTubeDownloader

del "YoutubeDownloader.exe"
del "YoutubeDownloader.exe.spec"
del "pylint.log"
del "geckodriver.log"
rmdir /s/q "__pycache__"
rmdir /s/q "build"
rmdir /s/q "Download"