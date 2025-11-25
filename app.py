# Status by Aaron Mairel

import customtkinter as ctk
from PIL import Image
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("red")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Status - Workout Tracker")
        self.geometry("800x465")
        self.resizable(False, False)

        long_logo = ctk.CTkImage(
            light_image=Image.open("resources/mainlogo.png"),
            dark_image=Image.open("resources/mainlogo.png"),
            size=(123, 67)
        )

        self.logoframe = ctk.CTkFrame(self, width=150, height=65)
        self.logoframe.place(x=20,y=20)

        self.barframe = ctk.CTkFrame(self, width=150, height=355)
        self.barframe.place(x=20, y=95)

        self.mainframe = ctk.CTkFrame(self, width=565, height=415)
        self.mainframe.place(x=200, y=20)

        self.homeframe = ctk.CTkFrame(self.mainframe, width=545, height=400, fg_color="#212121")
        self.homeframe.pack(padx=15, pady=15)

        self.calendarbox = ctk.CTkScrollableFrame(self.homeframe, height=160, width=510, orientation="horizontal", fg_color="#212121")
        self.calendarbox.place(x=5, y=0)

        # Get the scrollable parent
        frame = self._get_scrollable_parent(self.calendarbox)

        current_datetime = datetime.now()
        weekday = current_datetime.weekday()

        # Get the scrollable parent
        frame = self._get_scrollable_parent(self.calendarbox)

        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        day_box_names = ["mondaybox", "tuesdaybox", "wednesdaybox", "thursdaybox",
                         "fridaybox", "saturdaybox", "sundaybox"]
        day_label_names = ["mondaylabel", "tuesdaylabel", "wednesdaylabel", "thursdaylabel",
                           "fridaylabel", "saturdaylabel", "sundaylabel"]

        for i, (day_name, box_name, label_name) in enumerate(zip(day_names, day_box_names, day_label_names)):
            day_container = ctk.CTkFrame(frame, fg_color="transparent")
            day_container.grid(row=0, column=i, padx=10, pady=0)

            day_label = ctk.CTkLabel(day_container, text=day_name, font=("Arial", 12, "bold"))
            day_label.pack(pady=(0, 3))
            setattr(self, label_name, day_label)

            outline_frame = ctk.CTkFrame(day_container, fg_color="#161616", corner_radius=8)
            outline_frame.pack()

            day_box = ctk.CTkLabel(outline_frame, width=120, height=100, text="", fg_color="#292929")
            day_box.pack(padx=4, pady=4)
            setattr(self, box_name, day_box)

        self.day_boxes = [getattr(self, name) for name in day_box_names]
        self.day_labels = [getattr(self, name) for name in day_label_names]

        self.day_labels[weekday].configure(text_color="#D72627")

        self.update()
        self.calendarbox._parent_canvas.xview_moveto(0.07*weekday)

        logo_label = ctk.CTkLabel(self.logoframe, image=long_logo, text="")

        logo_label.image = long_logo
        logo_label.place(x=13, y=-1)

        self.homebutton = ctk.CTkButton(self.barframe, text="Home", width=130, command=lambda: self.pick("home"))
        self.homebutton.place(x=10,y=20)

        self.routinebutton = ctk.CTkButton(self.barframe, text="Routine", width=130, command=lambda: self.pick("routine"))
        self.routinebutton.place(x=10, y=80)

        self.workoutbutton = ctk.CTkButton(self.barframe, text="Workout Log", width=130, command=lambda: self.pick("workout"))
        self.workoutbutton.place(x=10, y=140)

        self.profilebutton = ctk.CTkButton(self.barframe, text="Profile", width=130, command=lambda: self.pick("profile"))
        self.profilebutton.place(x=10, y=200)

        self.settingsbutton = ctk.CTkButton(self.barframe, text="Settings", width=130, state="disabled", command=lambda: self.pick("settings"))
        self.settingsbutton.place(x=10, y=260)

    def pick(self,frame):
        if frame == "home":
            self.homeframe.pack(padx=15,pady=15)
        elif frame == "routine":
            print("meow")
            self.homeframe.pack_forget()
        elif frame == "workout":
            print("moo")
        elif frame == "profile":
            print("cheep")

    # def outline(self, widget, padding=5, color="black"):
    #     info = widget.place_info()
    #     x = int(info["x"])
    #     y = int(info["y"])
    #
    #     widget.update_idletasks()
    #     w = widget.winfo_width()
    #     h = widget.winfo_height()
    #     widget.place_forget()
    #
    #     parent = widget.master  # the actual parent where the widget was placed
    #
    #     outline_frame = ctk.CTkFrame(
    #         master=parent,
    #         width=w + padding * 2,
    #         height=h + padding * 2,
    #         fg_color=color,
    #         corner_radius=8
    #     )
    #     outline_frame.place(x=x - padding, y=y - padding)
    #
    #     # place the widget back inside the outline (or as sibling if you prefer)
    #     widget.place(in_=outline_frame, x=padding, y=padding)
    #     widget.lift()

    import tkinter as tk  # needed for isinstance checks

    def _get_scrollable_parent(self, scrollable):
        for name in ("scrollable_frame", "frame", "inner_frame", "_frame", "_inner_frame"):
            if hasattr(scrollable, name):
                return getattr(scrollable, name)

        for child in scrollable.winfo_children():
            if isinstance(child, (ctk.CTkFrame, tk.Frame)):
                return child

        return scrollable


if __name__ == "__main__":
    app = App()
    app.mainloop()