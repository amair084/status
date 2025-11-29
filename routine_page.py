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
        self.temp_routine = {}
        self.secondPage = False

        self.place(relwidth=1, relheight=1)

        self.homeframe = ctk.CTkFrame(self, width=545, height=425, fg_color="#29292A")
        self.homeframe.pack(padx=15, pady=15)

        self.backbutton = ctk.CTkButton(self.homeframe, text="Back", command=self.reset, width=100)
        self.changebutton = ctk.CTkButton(self.homeframe, text="Add Routine", width=100, height=30, command=self.add_routine)
        self.nextpagebutton = ctk.CTkButton(self.homeframe, text="Next Page", width=50, height=17)
        self.activebutton = ""

        # Day buttons
        self.mondaybutton = ctk.CTkButton(self.homeframe, text="Monday")
        self.tuesdaybutton = ctk.CTkButton(self.homeframe, text="Tuesday")
        self.wednesdaybutton = ctk.CTkButton(self.homeframe, text="Wednesday")
        self.thursdaybutton = ctk.CTkButton(self.homeframe, text="Thursday")
        self.fridaybutton = ctk.CTkButton(self.homeframe, text="Friday")
        self.saturdaybutton = ctk.CTkButton(self.homeframe, text="Saturday")
        self.sundaybutton = ctk.CTkButton(self.homeframe, text="Sunday")

        self.days = [self.mondaybutton, self.tuesdaybutton, self.wednesdaybutton,
                     self.thursdaybutton, self.fridaybutton, self.saturdaybutton,
                     self.sundaybutton]

        self.reset()

    # ---------------------- ROUTINE SAVING ----------------------
    def add_routine(self):
        if not self.activebutton:
            return

        # Save currently visible entries (current page)
        self.save_current_page_entries(self.secondPage)

        day_name = self.activebutton.cget("text")
        movements_dict = {}

        # Save all temp_routine entries (both pages)
        for movement_name, (sets, reps) in self.temp_routine.items():
            if sets and reps:
                try:
                    movements_dict[movement_name] = (int(sets), int(reps))
                except ValueError:
                    continue

        self.data.save_routine(day_name, movements_dict)
        print(f"Routine saved for {day_name}: {movements_dict}")

        self.reset()

    def save_current_page_entries(self, secondPage=False):
        """Save the entries currently displayed to temp_routine."""
        workouts = WorkoutData.movements(self)
        start_index = 0 if not secondPage else 12
        end_index = min(12, len(workouts)) if not secondPage else len(workouts)

        for local_i, i in enumerate(range(start_index, end_index)):
            movement_name = workouts[i]
            sets = self.set_entries[local_i].get().strip()
            reps = self.rep_entries[local_i].get().strip()

            if sets or reps:
                # Save or update
                self.temp_routine[movement_name] = (sets, reps)
            elif movement_name in self.temp_routine:
                # Remove if both entries are empty
                del self.temp_routine[movement_name]

    # ---------------------- LOAD WORKOUTS ----------------------
    def load_workouts(self, secondPage=False):
        self.secondPage = secondPage
        workouts = WorkoutData.movements(self)

        # Switch page command
        self.nextpagebutton.configure(command=lambda:self.load_workouts(not secondPage))

        # Clear old widgets
        for widget in self.labels:
            widget.destroy()
        self.labels = []
        self.set_entries = []
        self.rep_entries = []

        # Determine which movements to show
        start_index = 0 if not secondPage else 12
        end_index = min(12, len(workouts)) if not secondPage else len(workouts)

        saved_routine = {}
        if self.activebutton:
            day_name = self.activebutton.cget("text")
            saved_routine = self.data.db.load_routine(day_name)

        left_x = 0
        right_x = 260
        start_y = 65
        row_height = 45

        for local_i, i in enumerate(range(start_index, end_index)):
            movement_name = workouts[i]
            x = left_x if local_i % 2 == 0 else right_x
            row = local_i // 2
            y = start_y + row * row_height

            # Font sizing based on name length
            text_len = len(movement_name)
            font_size = 12
            width = 70
            if text_len > 13:
                font_size = 8
            elif text_len > 12:
                font_size = 9
            elif text_len > 10:
                font_size = 11

            # Labels and entry boxes
            label1 = ctk.CTkButton(self.homeframe, text=movement_name + ":", font=("Arial", font_size), width=width)
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

            # Insert previously saved values from temp_routine or db
            if movement_name in self.temp_routine:
                sets, reps = self.temp_routine[movement_name]
                entry_sets.insert(0, str(sets))
                entry_reps.insert(0, str(reps))
            elif movement_name in saved_routine:
                sets, reps = saved_routine[movement_name]
                entry_sets.insert(0, str(sets))
                entry_reps.insert(0, str(reps))

            self.labels.extend([label1, label2, label3, entry_sets, entry_reps])

        self.nextpagebutton.place(x=430, y=325)
        self.changebutton.place(x=195, y=345)

    # ---------------------- PICK DAY ----------------------
    def pick(self, button):
        self.backbutton.place(x=10, y=5)
        for x in self.days:
            x.place_forget()
        button.place(x=195, y=5)
        button.configure(width=120, command=None)
        self.activebutton = button
        self.temp_routine = {}

        # Load saved routine
        day_name = button.cget("text")
        saved_routine = self.data.db.load_routine(day_name)
        for movement_name, (sets, reps) in saved_routine.items():
            self.temp_routine[movement_name] = (sets, reps)

        self.load_workouts()

    # ---------------------- RESET ----------------------
    def reset(self):
        current = 50
        self.backbutton.place_forget()
        self.changebutton.place_forget()
        self.nextpagebutton.place_forget()

        for widget in self.labels:
            widget.destroy()
        self.labels = []
        self.rep_entries = []
        self.set_entries = []

        for x in self.days:
            x.place_forget()

        for x in self.days:
            x.configure(width=70, command=lambda d=x: self.pick(d))
            if x in [self.days[4], self.days[5], self.days[6]]:
                x.place(x=current - 350, y=50)
            else:
                x.place(x=current, y=5)
            current += 100
