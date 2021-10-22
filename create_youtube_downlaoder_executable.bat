:: "generate_youtube_downloader_executable.bat"
:: generate execuatable file for youtube downloader

pyinstaller youtube_downloader.pyw --clean --onefile -i"app.ico" --name YouTubeDownloader.exe --distpath ./

pause