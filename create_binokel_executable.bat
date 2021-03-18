:: "generate_youtube_downloader_executable.bat"
:: generate execuatable file for youtube downloader

pyinstaller youtube_downloader.pyw --clean --onefile -i"Tool/app.ico" --name YouTubeDownloader.exe --distpath Tool

pause