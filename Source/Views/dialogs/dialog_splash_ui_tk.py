"""!
*****************************************************************************
@file   dialog_splash_ui_tk.py
@brief  Splash screen with tkinter
*****************************************************************************
"""

from tkinter import Label


class Ui_SplashScreen(object):
    def setupUi(self, SplashScreen):
        SplashScreen.title("SplashScreen")
        SplashScreen.geometry("800x514")
        SplashScreen.overrideredirect(True)  # Remove window decorations (title bar, close button)

        # Center the splash screen on the screen
        SplashScreen.update_idletasks()
        width = SplashScreen.winfo_width()
        height = SplashScreen.winfo_height()
        x = (SplashScreen.winfo_screenwidth() // 2) - (width // 2)
        y = (SplashScreen.winfo_screenheight() // 2) - (height // 2)
        SplashScreen.geometry(f"{width}x{height}+{x}+{y}")

        self.lbl_icon_placeholder = Label(SplashScreen)
        self.lbl_icon_placeholder.place(x=0, y=0, width=800, height=514)

        self.lbl_productName = Label(SplashScreen, text="YouTubeDownloader", font=("Helvetica", 24, "bold"))
        self.lbl_productName.place(x=440, y=70, width=351, height=61)

        self.lbl_version = Label(SplashScreen, text="1.0.0", font=("Helvetica", 18, "bold"))
        self.lbl_version.place(x=510, y=180, width=171, height=61)

        self.lbl_software_text = Label(SplashScreen, text="Software", font=("Helvetica", 18, "bold"))
        self.lbl_software_text.place(x=440, y=140, width=131, height=31)

        self.lbl_version_text = Label(SplashScreen, text="Version", font=("Helvetica", 18, "bold"))
        self.lbl_version_text.place(x=490, y=170, width=131, height=31)
