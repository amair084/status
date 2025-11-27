from logging import setLogRecordFactory

import customtkinter as ctk
from datetime import datetime
import ui_components
from data import WorkoutData


class RoutinePage(ctk.CTkFrame):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data

        self.labels = []
        self.set_entries = []
        self.rep_entries = []

        self.place(relwidth=1, relheight=1)

        self.homeframe = ctk.CTkFrame(self, width=545, height=425, fg_color="#29292A")
        self.homeframe.pack(padx=15, pady=15)

        self.backbutton = ctk.CTkButton(self.homeframe, text="Back", command=self.reset, width=100)
        self.changebutton = ctk.CTkButton(self.homeframe, text="Add Routine", width=100, height=20, command=self.add_routine)
        self.activebutton = ""

        self.mondaybutton = ctk.CTkButton(self.homeframe, text="Monday")
        self.tuesdaybutton = ctk.CTkButton(self.homeframe, text="Tuesday")
        self.wednesdaybutton = ctk.CTkButton(self.homeframe, text="Wednesday")
        self.thursdaybutton = ctk.CTkButton(self.homeframe, text="Thursday")
        self.fridaybutton = ctk.CTkButton(self.homeframe, text="Friday")
        self.saturdaybutton = ctk.CTkButton(self.homeframe, text="Saturday")
        self.sundaybutton = ctk.CTkButton(self.homeframe, text="Sunday")


        self.days = [self.mondaybutton, self.tuesdaybutton, self.wednesdaybutton,
                self.thursdaybutton, self.fridaybutton, self.saturdaybutton,
                self.sundaybutton
                ]

        self.reset()

    def add_routine(self):
        if not self.activebutton:
            return

        day_name = self.activebutton.cget("text")

        movements_dict = {}
        for i, movement_name in enumerate(WorkoutData.movements(self)):
            sets = self.set_entries[i].get().strip()
            reps = self.rep_entries[i].get().strip()

            if sets and reps:
                try:
                    movements_dict[movement_name] = (int(sets), int(reps))
                except ValueError:
                    continue

        # Save to WorkoutData

        self.data.save_routine(day_name, movements_dict)

        print(f"Routine saved for {day_name}: {movements_dict}")

        self.reset()

    def load_workouts(self):
        workouts = WorkoutData.movements(self)

        # layout constants (adjust if needed)
        left_x = 0
        right_x = 260
        start_y = 50
        row_height = 40

        for i, name in enumerate(workouts):
            if i % 2 == 0:
                x = left_x
            else:
                x = right_x

            row = i // 2
            y = start_y + row * row_height

            text_len = len(name)
            if text_len > 13:
                font_size = 8
                width = 70
            elif text_len > 12:
                font_size = 9
                width = 70
            elif text_len > 10:
                font_size = 11
                width = 70
            else:
                font_size = 12
                width = 70

            label1 = ctk.CTkButton(
                self.homeframe,
                text=name + ":",
                font=("Arial", font_size),
                width=width
            )
            label1.place(x=x, y=y)

            label2 = ctk.CTkLabel(self.homeframe, text="Sets:")
            label2.place(x=x + width + 20, y=y)

            entry_sets = ctk.CTkEntry(self.homeframe, width=35)
            entry_sets.place(x=x + width + 60, y=y)

            self.set_entries.append(entry_sets)

            label3 = ctk.CTkLabel(self.homeframe, text="Reps:")
            label3.place(x=x + width + 100, y=y)

            entry_reps = ctk.CTkEntry(self.homeframe, width=35)
            entry_reps.place(x=x + width + 140, y=y)

            self.rep_entries.append(entry_reps)

            self.labels.extend([label1, label2, label3, entry_sets, entry_reps])

        self.changebutton.place(x=195,y=355)



    def pick(self, button):
        self.backbutton.place(x=10,y=5)
        for x in self.days:
            x.place_forget()
        button.place(x=195, y=5)
        button.configure(width=120, command=None)
        self.activebutton = button
        self.load_workouts()

        day_name = button.cget("text")
        saved_routine = self.data.db.load_routine(day_name)
        for i, movement_name in enumerate(WorkoutData.movements(self)):
            if movement_name in saved_routine:
                sets, reps = saved_routine[movement_name]
                self.set_entries[i].delete(0, "end")
                self.set_entries[i].insert(0, str(sets))
                self.rep_entries[i].delete(0, "end")
                self.rep_entries[i].insert(0, str(reps))

    def reset(self):
        current = 50
        self.backbutton.place_forget()
        self.changebutton.place_forget()

        for widget in self.labels:
            widget.destroy()
        self.labels = []
        self.rep_entries = []
        self.set_entries = []

        for x in self.days:
            x.place_forget()

        for x in self.days:
            x.configure(width=70, command=lambda d=x: self.pick(d))
            if x == self.days[4] or x == self.days[5] or x == self.days[6]:
                x.place(x=current - 350, y=50)
            else:
                x.place(x=current,y=5)
            current +=100