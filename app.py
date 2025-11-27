# Status by Aaron Mairel
from datetime import datetime

import customtkinter as ctk
from PIL import Image
from bar_ui import BarMenu
from home_page import HomePage
from routine_page import RoutinePage
from log_page import LogWorkoutPage
from data import WorkoutData

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("red")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Status - Workout Tracker")
        self.geometry("800x465")
        self.resizable(False, False)

        self.mainframe = ctk.CTkFrame(self, width=565, height=430)
        self.mainframe.place(x=200, y=20)

        self.data = WorkoutData()
        self.data.db = WorkoutData("workouts.db")

        # today = datetime.today()
        #
        # formatted_date = today.strftime("%d/%m/%Y")
        # print(formatted_date)


        self.barframe = BarMenu(self, callback=self.switch_page)
        self.barframe.place(x=0, y=0)
        self.barframe.configure(width=200,height=465, fg_color="#1A1A1A")

        self.homepage = HomePage(self.mainframe, self.data)
        self.homepage.place(relwidth=0.95, relheight=0.95, x=15, y=10)

        self.routinepage = RoutinePage(self.mainframe, self.data)

        self.logworkoutpage = LogWorkoutPage(self.mainframe, self.data)

        self.pages = {
            "home": self.homepage,
            "routine": self.routinepage,
            "log": self.logworkoutpage
        }

        self.homepage.lift()

    def switch_page(self, page_name):
        for x in self.pages.values():
            x.place_forget()
        page = self.pages[page_name]
        page.place(relwidth=0.95, relheight=0.95, x=15, y=10)

        if hasattr(page, "refresh"):
            page.refresh()





if __name__ == "__main__":
    app = App()
    app.mainloop()