import customtkinter as ctk
from datetime import datetime
import ui_components
from data import WorkoutData

class LogWorkoutPage(ctk.CTkFrame):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.place(relwidth=1, relheight=1)

        self.movements_list = []
        self.sets_list = []
        self.reps_list = []

        self.homeframe = ctk.CTkScrollableFrame(self, width=545, height=425, fg_color="#29292A")
        self.homeframe.pack(padx=15, pady=15)

        self.container = ctk.CTkFrame(self.homeframe, height=100, width=200, corner_radius=10, fg_color="#212121")

        self.box = ctk.CTkFrame(self.container, height=150, width=325, corner_radius=10, fg_color="#29292A")

        spacer = ctk.CTkFrame(self.homeframe, height=250, fg_color="transparent")
        spacer.pack(fill="x")

        self.y = 10

        self.entrybutton = ctk.CTkButton(self,width=30,height=25, fg_color="#212121", text="+", font=("Arial", 20, "bold"), text_color="#8D1F1F", command=self.entry)
        self.entrybutton.place(x=460,y=365)

        self.display_logs()

    def display_logs(self):
        logs = self.load_logs()

        y_offset = 15

        for date, log in logs.items():

            date_container = ctk.CTkFrame(self.homeframe, height=50 +17*len(log), width=450, corner_radius=10, fg_color="#212121")
            date_box = ctk.CTkFrame(date_container, height=50 +17*len(log), width=450, corner_radius=10, fg_color="#29292A")
            date_container.pack_propagate(False)
            date_box.pack_propagate(False)

            logged_date = datetime.strptime(date, "%Y-%m-%d").date()
            today = datetime.today().date()

            days_ago = (today - logged_date).days

            date_label = ctk.CTkLabel(date_container, text=date+f"  • {days_ago} days ago", font=("Arial", 12, "bold"))
            if days_ago == 0:
                date_label.configure(text=date+f"  •  Today")

            date_label.pack(pady=1)

            date_container.place(x=20, y=y_offset)
            date_box.pack(padx=4, pady=4)

            left_x = 0
            right_x = 260
            row_height = 30
            start_y = 5

            i = 0
            for a in log:
                if len(log) > 5:
                    if i % 2 == 0:
                        x = left_x
                    else:
                        x = right_x

                    row = i // 2
                    y = start_y + row * row_height

                    movement_label = ctk.CTkLabel(date_box, text=f"{a['movement']}: {a['sets']}x{a['reps']}",
                                                  font=("Arial", 12))
                    movement_label.place(x=x, y=y)

                    i += 1


    def load_logs(self):
        all_logs = self.data.load_logs()

        logs_by_date = {}

        for log in all_logs:
            print(f"{log['date']}: {log['movement']} - {log['sets']}x{log['reps']}")
            date = log['date']
            if date not in logs_by_date:
                logs_by_date[date] = []
            logs_by_date[date].append(log)

        return logs_by_date

    def hi(self):
        self.after(50, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        canvas = self.homeframe._parent_canvas
        if canvas.bbox("all") is None:
            self.after(10, self.scroll_to_bottom)
            return
        canvas.yview_moveto(1.0)


    def entry(self):
        self.scroll_to_bottom()

        if not hasattr(self, "streakcontainer"):

            spacer = ctk.CTkFrame(self.homeframe, height=50, fg_color="transparent")
            spacer.pack(fill="x")

            self.day_label = ctk.CTkLabel(self.homeframe, text="Log Workout", font=("Arial", 12, "bold"))
            self.day_label.pack(pady=0)

            self.streakcontainer = ctk.CTkFrame(self.homeframe, height=100, width=250, corner_radius=10, fg_color="#212121")
            self.streakcontainer.pack(padx=25, pady=0)

            self.streakbox = ctk.CTkScrollableFrame(self.streakcontainer,scrollbar_fg_color="#29292A" ,height=150, width=355, corner_radius=10, fg_color="#29292A")
            self.streakbox.pack(padx=5, pady=5)

            spacer = ctk.CTkFrame(self.homeframe, height=50, fg_color="transparent")
            spacer.pack(fill="x")

            self.after(50,self.scroll_to_bottom)

            self.workout_entry(self.streakbox)

            self.confirm_button = ctk.CTkButton(
                self,
                text="Confirm Workout",
                fg_color="#8D1F1F",
                command=self.confirm
            )
            self.confirm_button.place(relx=0.5, rely=0.92, anchor="s")


    def confirm(self):
        today = datetime.now().strftime("%Y-%m-%d")


        print([x.get() for x in self.movements_list])
        print([x.get() for x in self.sets_list])
        print([x.get() for x in self.reps_list])

        for movement, sets, reps in zip(self.movements_list, self.sets_list, self.reps_list):
            if reps.get() and reps.get().isdigit() and sets.get() and sets.get().isdigit():

                print("Confirmed!")
                self.confirm_button.place_forget()

                self.data.log_workout(today, movement.get(), sets.get(), reps.get())

                if hasattr(self, "streakcontainer"):
                    self.streakcontainer.destroy()
                    del self.streakcontainer

                self.day_label.destroy()

                if hasattr(self, "day_label"):
                    self.day_label.destroy()

                self.confirm_button.place_forget()

                self.movements_list.clear()
                self.sets_list.clear()
                self.reps_list.clear()
                self.y = 10

        self.display_logs()

    def workout_entry(self, b, confirm=""):
        workouts = WorkoutData.movements(self)

        self.dropdown = ctk.CTkOptionMenu(b, values=workouts)
        self.dropdown.pack(padx=10, pady=10, anchor="w")
        self.movements_list.append(self.dropdown)

        print(self.dropdown.get())

        self.label2 = ctk.CTkLabel(b, text="Sets:")
        self.label2.place(x=155, y=self.y)

        self.entry_sets = ctk.CTkEntry(b, width=35)
        self.entry_sets.place(x=190, y=self.y)
        self.sets_list.append(self.entry_sets)

        self.label3 = ctk.CTkLabel(b, text="Reps:")
        self.label3.place(x=230, y=self.y)

        self.entry_reps = ctk.CTkEntry(b, width=35)
        self.entry_reps.place(x=265, y=self.y)
        self.reps_list.append(self.entry_reps)

        self.confirmbutton = ctk.CTkButton(b, width=24, height=22, fg_color="#212121", text="+",
                                         font=("Arial", 16, "bold"), text_color="#8D1F1F", command= lambda: self.workout_entry(b, self.confirmbutton))
        self.confirmbutton.place(x=320, y=11+(self.y-10))

        if confirm != "":
            confirm.destroy()

        self.y += 48


