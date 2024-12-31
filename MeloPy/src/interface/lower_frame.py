from tkinter import Button, Frame, PhotoImage, Label, Scale, HORIZONTAL, FLAT
from pathlib import Path
from PIL import ImageTk
import PIL.Image

FOREGROUND = "#d6d6d6"

class LowerFrame(Frame):
    def __init__(self, parent, max_width, max_height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icons = []
        self.widgets = []
        self.assets = Path(__file__).parent.joinpath("assets/lower_frame")
        self.max_width, self.max_height = max_width, max_height
        self.parent = parent
        self.initialize()

    def initialize(self):
        background = "#353535"

        previous_icon = self.assets.joinpath("previous-50.png")
        self.icons.append(PhotoImage(file=previous_icon))

        play_icon = self.assets.joinpath("play-50.png")
        self.icons.append(PhotoImage(file=play_icon))

        next_icon = self.assets.joinpath("next-50.png")
        self.icons.append(PhotoImage(file=next_icon))

        stop_icon = self.assets.joinpath("stop-50.png")
        self.icons.append(PhotoImage(file=stop_icon))

        mute_icon = self.assets.joinpath("mute-50.png")
        self.icons.append(PhotoImage(file=mute_icon))

        shuffle_icon = self.assets.joinpath("shuffle-50.png")
        self.icons.append(PhotoImage(file=shuffle_icon))

        repeat_icon = self.assets.joinpath("repeat-50.png")
        self.icons.append(PhotoImage(file=repeat_icon))

        forward_5_icon = self.assets.joinpath("forward-5-50.png")
        self.icons.append(PhotoImage(file=forward_5_icon))

        backward_5_icon = self.assets.joinpath("backward-5-50.png")
        self.icons.append(PhotoImage(file=backward_5_icon))

        image_path = self.assets.joinpath("lana.jpg").open("rb")
        image = PIL.Image.open(image_path)
        image = image.resize((175, 175))
        self.icons.append(ImageTk.PhotoImage(image))

        singer_icon = self.assets.joinpath("singer-25.png")
        self.icons.append(PhotoImage(file=singer_icon))

        album_icon = self.assets.joinpath("album-25.png")
        self.icons.append(PhotoImage(file=album_icon))

        song_icon = self.assets.joinpath("song-25.png")
        self.icons.append(PhotoImage(file=song_icon))

        frame = Frame(master=self.parent, background=background, border=0, height=self.max_height // 8, width=self.max_width)
        frame.place(rely=0.88)

        previous_button = Button(master=frame, background=background, image=self.icons[0], border=0,
                                 highlightthickness=False)
        previous_button.place(relx=0.45, rely=0.27)

        play_button = Button(master=frame, background=background, image=self.icons[1], border=0,
                             highlightthickness=False)
        play_button.place(relx=0.48, rely=0.27)

        next_button = Button(master=frame, background=background, image=self.icons[2], border=0,
                             highlightthickness=False)
        next_button.place(relx=0.51, rely=0.27)

        stop_button = Button(master=frame, background=background, image=self.icons[3], border=0,
                             highlightthickness=False)
        stop_button.place(relx=0.395, rely=0.27)

        mute_button = Button(master=frame, background=background, image=self.icons[4], border=0,
                             highlightthickness=False)
        mute_button.place(relx=0.565, rely=0.27)

        shuffle_button = Button(master=frame, background=background, image=self.icons[5], border=0,
                                highlightthickness=False)
        shuffle_button.place(relx=0.91, rely=0.53)

        repeat_button = Button(master=frame, background=background, image=self.icons[6], border=0,
                               highlightthickness=False)
        repeat_button.place(relx=0.94, rely=0.53)

        forward_5_button = Button(master=frame, background=background, image=self.icons[7], border=0,
                                  highlightthickness=False)
        forward_5_button.place(relx=0.536, rely=0.27)

        backward_5_button = Button(master=frame, background=background, image=self.icons[8], border=0,
                                   highlightthickness=False)
        backward_5_button.place(relx=0.425, rely=0.27)

        artist_image = Label(master=frame, image=self.icons[9])
        artist_image.place(relx=0.004, rely=0.1)

        singer_name = Label(master=frame, text="Lana Del Rey", font=("Arial", 15), background=background,
                            foreground=FOREGROUND)
        singer_name.place(relx=0.085, rely=0.15)

        singer_image = Label(master=frame, image=self.icons[10], background=background)
        singer_image.place(relx=0.072, rely=0.19)

        album_name = Label(master=frame, text="Lust For Life", font=("Arial", 15), background=background,
                           foreground=FOREGROUND)
        album_name.place(relx=0.085, rely=0.41)

        album_image = Label(master=frame, image=self.icons[11], background=background)
        album_image.place(relx=0.072, rely=0.45)

        song_name = Label(master=frame, text="Ultraviolence", font=("Arial", 15), background=background,
                          foreground=FOREGROUND)
        song_name.place(relx=0.085, rely=0.66)

        song_image = Label(master=frame, image=self.icons[12], background=background)
        song_image.place(relx=0.072, rely=0.69)

        slider = Scale(master=frame, border=5, orient=HORIZONTAL, from_=0, to=100, cursor="arrow", sliderrelief=FLAT,
                       background=background, highlightthickness=False, relief=FLAT,sliderlength=10,
                       length=self.max_width - 1250, width=20, foreground=FOREGROUND, borderwidth=0, showvalue=False)
        slider.place(relx=0.2, rely=0.6)

        self.widgets.append(frame)
