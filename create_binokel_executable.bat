:: "generate_youtube_downloader_executable.bat"
:: generate execuatable file for binokel

pyinstaller youtube_downloader.pyw --clean --onefile --name YouTubeDownloader.exe --distpath Tool

pause