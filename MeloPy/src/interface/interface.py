from pathlib import Path
from PIL import ImageTk
from tkinter import *
import PIL.Image

BACKGROUND = "#1f1f1f"
FOREGROUND = "#d6d6d6"
ASSETS_PATH = Path(__file__).parent.parent.parent.joinpath("assets/")

class Interface(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slider = None
        self.static_modules = []
        self.lower_modules = []
        self.max_height, self.max_width = self.winfo_screenheight(), self.winfo_screenwidth()
        self.base_init()
        self.lower_widgets()

    def base_init(self):
        self.title("MeloPy")
        self.attributes("-fullscreen", True)
        self.configure(background=BACKGROUND)

    def lower_widgets(self):
        background = "#353535"

        previous_icon = ASSETS_PATH.joinpath("previous-50.png")
        self.static_modules.append(PhotoImage(file=previous_icon))

        play_icon = ASSETS_PATH.joinpath("play-50.png")
        self.static_modules.append(PhotoImage(file=play_icon))

        next_icon = ASSETS_PATH.joinpath("next-50.png")
        self.static_modules.append(PhotoImage(file=next_icon))

        stop_icon = ASSETS_PATH.joinpath("stop-50.png")
        self.static_modules.append(PhotoImage(file=stop_icon))

        mute_icon = ASSETS_PATH.joinpath("mute-50.png")
        self.static_modules.append(PhotoImage(file=mute_icon))

        shuffle_icon = ASSETS_PATH.joinpath("shuffle-50.png")
        self.static_modules.append(PhotoImage(file=shuffle_icon))

        repeat_icon = ASSETS_PATH.joinpath("repeat-50.png")
        self.static_modules.append(PhotoImage(file=repeat_icon))

        forward_5_icon = ASSETS_PATH.joinpath("forward-5-50.png")
        self.static_modules.append(PhotoImage(file=forward_5_icon))

        backward_5_icon = ASSETS_PATH.joinpath("backward-5-50.png")
        self.static_modules.append(PhotoImage(file=backward_5_icon))

        image_path = ASSETS_PATH.joinpath("lana.jpg").open("rb")
        image = PIL.Image.open(image_path)
        image = image.resize((150, 150))
        self.static_modules.append(ImageTk.PhotoImage(image))

        singer_icon = ASSETS_PATH.joinpath("singer-25.png")
        self.static_modules.append(PhotoImage(file=singer_icon))

        album_icon = ASSETS_PATH.joinpath("album-25.png")
        self.static_modules.append(PhotoImage(file=album_icon))

        song_icon = ASSETS_PATH.joinpath("song-25.png")
        self.static_modules.append(PhotoImage(file=song_icon))

        frame = Frame(master=self, background=background, border=0, height=self.max_height // 8, width=self.max_width)
        frame.place(rely=0.88)

        previous_button = Button(master=frame, background=background, image=self.static_modules[0], border=0,
                                 highlightthickness=False)
        previous_button.place(relx=0.45, rely=0.6)

        play_button = Button(master=frame, background=background, image=self.static_modules[1], border=0,
                             highlightthickness=False)
        play_button.place(relx=0.48, rely=0.6)

        next_button = Button(master=frame, background=background, image=self.static_modules[2], border=0,
                             highlightthickness=False)
        next_button.place(relx=0.51, rely=0.6)

        stop_button = Button(master=frame, background=background, image=self.static_modules[3], border=0,
                             highlightthickness=False)
        stop_button.place(relx=0.395, rely=0.6)

        mute_button = Button(master=frame, background=background, image=self.static_modules[4], border=0,
                             highlightthickness=False)
        mute_button.place(relx=0.565, rely=0.6)

        shuffle_button = Button(master=frame, background=background, image=self.static_modules[5], border=0,
                             highlightthickness=False)
        shuffle_button.place(relx=0.86, rely=0.6)

        repeat_button = Button(master=frame, background=background, image=self.static_modules[6], border=0,
                                highlightthickness=False)
        repeat_button.place(relx=0.885, rely=0.6)

        forward_5_button = Button(master=frame, background=background, image=self.static_modules[7], border=0,
                                     highlightthickness=False)
        forward_5_button.place(relx=0.536, rely=0.6)

        backward_5_button = Button(master=frame, background=background, image=self.static_modules[8], border=0,
                            highlightthickness=False)
        backward_5_button.place(relx=0.425, rely=0.6)


        artist_image = Label(master=frame, image=self.static_modules[9])
        artist_image.place(relx=0.004, rely=0.25)

        singer_name = Label(master=frame, text="Lana Del Rey", font=("Arial", 17), background=background,
                            foreground=FOREGROUND)
        singer_name.place(relx=0.075, rely=0.28)

        singer_image = Label(master=frame, image=self.static_modules[10], background=background)
        singer_image.place(relx=0.063, rely=0.31)

        album_name = Label(master=frame, text="Lust For Life", font=("Arial", 17), background=background, foreground=FOREGROUND)
        album_name.place(relx=0.075, rely=0.51)

        album_image = Label(master=frame, image=self.static_modules[11], background=background)
        album_image.place(relx=0.063, rely=0.55)

        song_name = Label(master=frame, text="Ultraviolence", font=("Arial", 17), background=background,
                          foreground=FOREGROUND)
        song_name.place(relx=0.075, rely=0.73)

        song_image = Label(master=frame, image=self.static_modules[12], background=background)
        song_image.place(relx=0.063, rely=0.76)

        self.slider = Scale(master=frame, border=5, orient=HORIZONTAL, from_=0, to=100, cursor="arrow", sliderrelief=FLAT,
                            background=background, highlightthickness=False, relief=FLAT, sliderlength=10,
                            length=self.max_width - 25, width=20, foreground=FOREGROUND, borderwidth=0, showvalue=False)
        self.slider.place(relx=0.0016, rely=0.1)

        self.lower_modules.append(frame)
