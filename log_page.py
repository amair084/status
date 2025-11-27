import customtkinter as ctk
from datetime import datetime
import ui_components
from data import WorkoutData

class LogWorkoutPage(ctk.CTkFrame):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.place(relwidth=1, relheight=1)

        self.homeframe = ctk.CTkScrollableFrame(self, width=545, height=425, fg_color="#29292A")
        self.homeframe.pack(padx=15, pady=15)

        self.container = ctk.CTkFrame(self.homeframe, height=100, width=200, corner_radius=10, fg_color="#212121")

        self.box = ctk.CTkFrame(self.container, height=150, width=325, corner_radius=10, fg_color="#29292A")

        self.streakcontainer = ctk.CTkFrame(self.homeframe, height=100, width=200, corner_radius=10, fg_color="#212121")

        spacer = ctk.CTkFrame(self.homeframe, height=250, fg_color="transparent")
        spacer.pack(fill="x")


        self.entrybutton = ctk.CTkButton(self,width=30,height=25, fg_color="#212121", text="+", font=("Arial", 20, "bold"), text_color="#8D1F1F", command=self.entry)
        self.entrybutton.place(x=460,y=365)

        # Scroll to bottom after UI loads
        self.after(50, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        canvas = self.homeframe._parent_canvas
        if canvas.bbox("all") is None:
            self.after(10, self.scroll_to_bottom)
            return
        canvas.yview_moveto(1.0)


    def entry(self):
        self.scroll_to_bottom()

        if self.streakcontainer.winfo_x() == 0:

            spacer = ctk.CTkFrame(self.homeframe, height=50, fg_color="transparent")
            spacer.pack(fill="x")

            day_label = ctk.CTkLabel(self.homeframe, text="Log Workout", font=("Arial", 12, "bold"))
            day_label.pack(pady=0)

            self.streakcontainer = ctk.CTkFrame(self.homeframe, height=100, width=250, corner_radius=10, fg_color="#212121")
            self.streakcontainer.pack(padx=25, pady=0)

            self.streakbox = ctk.CTkScrollableFrame(self.streakcontainer,scrollbar_fg_color="#29292A" ,height=150, width=355, corner_radius=10, fg_color="#29292A")
            self.streakbox.pack(padx=5, pady=5)

            spacer = ctk.CTkFrame(self.homeframe, height=50, fg_color="transparent")
            spacer.pack(fill="x")
