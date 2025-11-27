import customtkinter as ctk
from PIL import Image

class BarMenu(ctk.CTkFrame):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.place(x=0, y=0)

        long_logo = ctk.CTkImage(
            light_image=Image.open("resources/mainlogo.png"),
            dark_image=Image.open("resources/mainlogo.png"),
            size=(123, 59)
        )

        self.logoframe = ctk.CTkFrame(self, width=150, height=65)
        self.logoframe.place(x=20, y=20)

        self.barframe = ctk.CTkFrame(self, width=150, height=355)
        self.barframe.place(x=20, y=95)

        logo_label = ctk.CTkLabel(self.logoframe, image=long_logo, text="")
        logo_label.image = long_logo
        logo_label.place(x=13, y=-1)

        self.homebutton = ctk.CTkButton(self.barframe, text="Home", width=130, command=lambda: self.pick("home"))
        self.homebutton.place(x=10, y=20)

        self.routinebutton = ctk.CTkButton(self.barframe, text="Routine", width=130,
                                           command=lambda: self.pick("routine"))
        self.routinebutton.place(x=10, y=80)

        self.workoutbutton = ctk.CTkButton(self.barframe, text="Workout Log", width=130,
                                           command=lambda: self.pick("log"))
        self.workoutbutton.place(x=10, y=140)

        self.profilebutton = ctk.CTkButton(self.barframe, text="Profile", width=130,
                                           command=lambda: self.pick("profile"))
        self.profilebutton.place(x=10, y=200)

        self.settingsbutton = ctk.CTkButton(self.barframe, text="Settings", width=130, state="disabled",
                                            command=lambda: self.pick("settings"))
        self.settingsbutton.place(x=10, y=260)

    def pick(self, frame):
        self.callback(frame)