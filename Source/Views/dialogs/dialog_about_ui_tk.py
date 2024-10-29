"""!
*****************************************************************************
@file   dialog_about_ui_tk.py
@brief  About dialog with tkinter
*****************************************************************************
"""

from tkinter import ttk, Label


class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.title("AboutDialog")
        AboutDialog.geometry("429x266")

        self.horizontalLayout = ttk.Frame(AboutDialog)
        self.horizontalLayout.pack(fill="both", expand=True)

        self.verticalLayout_2 = ttk.Frame(self.horizontalLayout, padding=(20, 20, 20, 20))
        self.verticalLayout_2.pack(side="left")

        self.imagePlaceholder = Label(AboutDialog)
        self.imagePlaceholder.pack(anchor="n")
        # self.imagePlaceholder.place(x=20, y=70, width=120, height=120) # TODO

        self.verticalLayout = ttk.Frame(self.horizontalLayout)
        self.verticalLayout.pack(side="left", fill="both", expand=True)

        self.lbl_productName = Label(self.verticalLayout, text="Product Name", font=("Helvetica", 20, "bold"))
        self.lbl_productName.pack(anchor="w")

        self.lbl_productDescription = Label(self.verticalLayout, text="Product Description")
        self.lbl_productDescription.pack(anchor="w")

        self.lbl_version = Label(self.verticalLayout, text="Version")
        self.lbl_version.pack(anchor="w")

        self.lbl_copyright = Label(self.verticalLayout, text="Copyright")
        self.lbl_copyright.pack(anchor="w")

        self.lbl_licence = Label(self.verticalLayout, text="License")
        self.lbl_licence.pack(anchor="w")

        self.lbl_home = Label(self.verticalLayout, text="Home")
        self.lbl_home.pack(anchor="w")
