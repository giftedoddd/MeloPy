from tkinter import *
from .lower_frame import LowerFrame

BACKGROUND = "#1f1f1f"

class App(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_height, self.max_width = self.winfo_screenheight(), self.winfo_screenwidth()
        self.base_init()
        self.lower_frame = LowerFrame(parent=self, max_width=self.max_width, max_height=self.max_height)
        self.lower_frame.place()

    def base_init(self):
        self.title("MeloPy")
        self.attributes("-fullscreen", True)
        self.configure(background=BACKGROUND)