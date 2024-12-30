from pathlib import Path
from tkinter import *

BACKGROUND = "#1f1f1f"
FOREGROUND = "#d6d6d6"
ASSETS_PATH = Path(__file__).parent.parent.parent.joinpath("assets/")

class Interface(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_modules = []
        self.lower_modules = []
        self.max_height, self.max_width = self.winfo_screenheight(), self.winfo_screenwidth()
        self.base_init()
        # self.widgets_()
        self.lower_widgets()

    def base_init(self):
        self.title("MeloPy")
        self.attributes("-fullscreen", True)
        self.configure(background=BACKGROUND)

    def lower_widgets(self):
        background = "#353535"

        previous_icon = ASSETS_PATH.joinpath("previous-50.png")
        self.static_modules.append(PhotoImage(master=self, file=previous_icon))

        play_icon = ASSETS_PATH.joinpath("play-50.png")
        self.static_modules.append(PhotoImage(master=self, file=play_icon))

        next_icon = ASSETS_PATH.joinpath("next-50.png")
        self.static_modules.append(PhotoImage(master=self, file=next_icon))

        frame = Frame(master=self, background=background, border=0, height=self.max_height // 10, width=self.max_width)
        frame.place(rely=0.9)

        previous_button = Button(master=frame, background=background, image=self.static_modules[0], border=0, highlightthickness=False)
        previous_button.place(relx=0.45, rely=0.6)

        play_button = Button(master=frame, background=background, image=self.static_modules[1], border=0, highlightthickness=False)
        play_button.place(relx=0.48, rely=0.6)

        next_button = Button(master=frame, background=background, image=self.static_modules[2], border=0, highlightthickness=False)
        next_button.place(relx=0.51, rely=0.6)

        self.lower_modules.append(frame)
