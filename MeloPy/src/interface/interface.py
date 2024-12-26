from pathlib import Path
from tkinter import *

BACKGROUND = "#1f1f1f"
FOREGROUND = "#d6d6d6"
ASSETS_PATH = Path(__file__).parent.parent.parent.joinpath("assets/")

class Interface(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_modules = []
        self.max_height, self.max_width = self.winfo_screenheight(), self.winfo_screenwidth()
        self.base_init()
        self.make_widgets()

    def base_init(self):
        self.title("MeloPy")
        self.attributes("-fullscreen", True)
        self.configure(background=BACKGROUND, padx=30, pady=50)

    def make_widgets(self):
        image_path = ASSETS_PATH.joinpath("more.png")
        burger_button_image = PhotoImage(master=self, file=image_path)
