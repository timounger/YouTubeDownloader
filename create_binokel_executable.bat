:: "generate_youtube_downloader_executable.bat"
:: generate execuatable file for binokel

pyinstaller youtube_downloader.py --clean --onefile -i"Tool/app.ico" --name YouTubeDownloader.exe --distpath Tool

pause