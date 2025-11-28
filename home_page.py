from calendar import weekday

import customtkinter as ctk
from datetime import datetime
import ui_components
from PIL import Image

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.place(relwidth=1, relheight=1)

        current_datetime = datetime.now()
        weekday = current_datetime.weekday()

        self.restday = False

        self.restday = weekday in (2, 4, 6)

        self.homeframe = ctk.CTkFrame(self, width=545, height=425, fg_color="#29292A")
        self.homeframe.pack(padx=15, pady=15)

        self.calendarbox = ctk.CTkScrollableFrame(self.homeframe, height=150, width=510, orientation="horizontal", fg_color="#29292A")
        self.calendarbox.place(x=0, y=0)

        self.streakcontainer = ctk.CTkFrame(self.homeframe, height=100, width=200,corner_radius=10, fg_color="#212121")
        self.streakcontainer.place(x=25,y=235)

        self.streakbox = ctk.CTkFrame(self.streakcontainer, height=85, width=175, corner_radius=10,fg_color="#29292A")
        self.streakbox.pack(padx=5,pady=5)

        streak_logo = ctk.CTkImage(
            light_image=Image.open("resources/Streak.png"),
            dark_image=Image.open("resources/Streak.png"),
            size=(120, 90)
        )

        streak_label = ctk.CTkLabel(self.streakbox, image=streak_logo, text="")
        streak_label2 = ctk.CTkLabel(self.streakbox, text="Current Streak")

        self.streak_counter = ctk.CTkLabel(self.streakbox, text="0 days", text_color="red", font=("Roboto", 15))
        self.streak_counter.place(x=95, y=37)

        streak_label2.place(x=80,y=15)
        streak_label.image = streak_logo
        streak_label.place(x=-20, y=-5)

        # Daily Workout

        self.dailycontainer = ctk.CTkFrame(self.homeframe, height=200, width=170, corner_radius=10, fg_color="#212121")
        self.dailycontainer.place(x=325, y=180)

        self.dailybox = ctk.CTkFrame(self.dailycontainer, height=185, width=155, corner_radius=10, fg_color="#29292A")
        self.dailybox.pack(padx=5, pady=5)
        self.dailybox.pack_propagate(False)

        dailybox_logo = ctk.CTkImage(
            light_image=Image.open("resources/bicep.png"),
            dark_image=Image.open("resources/bicep.png"),
            size=(35, 40)
        )

        self.daily_label = ctk.CTkLabel(self.dailybox, image=dailybox_logo, text="")
        daily_label2 = ctk.CTkLabel(self.dailybox, text="Today's Workout", font=("Roboto", 14), text_color="red")

        self.daily_label.image = dailybox_logo
        self.daily_label.place(x=2, y=0)
        daily_label2.place(x=40, y=10)



        # Get the scrollable parent
        frame = ui_components._get_scrollable_parent(self.calendarbox)


        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        container_names = ["mondaycbox", "tuesdaycbox", "wednesdaycbox", "thursdaycbox",
                         "fridaycbox", "saturdaycbox", "sundaycbox"]
        day_box_names = ["mondaybox", "tuesdaybox", "wednesdaybox", "thursdaybox",
                         "fridaybox", "saturdaybox", "sundaybox"]
        day_label_names = ["mondaylabel", "tuesdaylabel", "wednesdaylabel", "thursdaylabel",
                           "fridaylabel", "saturdaylabel", "sundaylabel"]

        for i, (day_name, container_name, box_name, label_name) in enumerate(zip(day_names, container_names, day_box_names, day_label_names)):
            day_container = ctk.CTkFrame(frame, fg_color="transparent")
            day_container.grid(row=0, column=i, padx=10, pady=0)

            day_label = ctk.CTkLabel(day_container, text=day_name, font=("Arial", 12, "bold"))
            day_label.pack(pady=(0, 3))
            setattr(self, label_name, day_label)

            outline_frame = ctk.CTkFrame(day_container, fg_color="#212121", corner_radius=4)
            outline_frame.pack()
            setattr(self, container_name, outline_frame)

            day_box = ctk.CTkFrame(outline_frame, width=60, height=50, fg_color="#292929")
            day_box.pack(padx=4, pady=4)
            setattr(self, box_name, day_box)

            routine = data.db.load_routine(day_name)
            if routine:
                for move, (sets, reps) in routine.items():
                    label = ctk.CTkLabel(day_box, text=f"{move}: {sets}x{reps}", font=("Arial", 9, "bold"), height=2)
                    if sets != 0:
                        label.pack(anchor="nw", fill="x", expand=True, pady=4, padx=3)
            else:
                # Show default "Rest Day"
                day_box.pack_propagate(False)
                rest_label = ctk.CTkLabel(day_box, text="Rest Day", font=("Arial", 12, "bold"))
                rest_label.pack(expand=True)


        self.day_boxes = [getattr(self, name) for name in day_box_names]
        self.day_labels = [getattr(self, name) for name in day_label_names]
        self.container_boxes = [getattr(self,name) for name in container_names]

        daily_workout = ui_components.clone_day_box(self, weekday)
        if self.restday == True:
            daily_workout.pack(padx=20, pady=70)
        else:
            daily_workout.place(x=32,y=30)

        self.day_labels[weekday].configure(text_color="#D72627")
        self.container_boxes[weekday].configure(fg_color="#8D1F1F")

        self.daily_label.lift()

        self.update()

    def refresh(self):
        current_datetime = datetime.now()
        weekday = current_datetime.weekday()

        self.restday = weekday in (2, 4, 6)

        self.update_calendar()
        self.update_today_workout(weekday)

        for lbl in self.day_labels:
            lbl.configure(text_color="white")

        for cont in self.container_boxes:
            cont.configure(fg_color="#212121")

        self.day_labels[weekday].configure(text_color="#D72627")
        self.container_boxes[weekday].configure(fg_color="#8D1F1F")

        self.after(5, lambda: self.scroll_to_today())

    def scroll_to_today(self):
        print("done")
        current_datetime = datetime.now()
        weekday = current_datetime.weekday()

        canvas = self.calendarbox._parent_canvas

        if canvas.bbox("all") is None:
            self.after(20, self.scroll_to_today)
            return

        target = 0.05 * weekday

        self.after(40, lambda: canvas.xview_moveto(target))

    def update_calendar(self):
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        for i, day_name in enumerate(day_names):
            box = self.day_boxes[i]


            for child in box.winfo_children():
                child.destroy()

            routine = self.data.db.load_routine(day_name)

            if routine:
                for move, (sets, reps) in routine.items():
                    if sets != 0:
                        label = ctk.CTkLabel(
                            box,
                            text=f"{move}: {sets}x{reps}",
                            font=("Arial", 9, "bold"),
                            height=2
                        )
                        label.pack(anchor="nw", fill="x", expand=True, pady=4, padx=3)
            else:
                rest_label = ctk.CTkLabel(box, text="Rest Day", font=("Arial", 12, "bold"))
                rest_label.pack(expand=True)

    def update_today_workout(self, weekday):
        # Clear previous daily workout box
        for child in self.dailybox.winfo_children():
            child.destroy()

        cloned = ui_components.clone_day_box(self, weekday)

        if self.restday:
            cloned.pack(padx=20, pady=70)
        else:
            cloned.place(x=30, y=30)

        dailybox_logo = ctk.CTkImage(
            light_image=Image.open("resources/bicep.png"),
            dark_image=Image.open("resources/bicep.png"),
            size=(35, 40)
        )

        self.daily_label = ctk.CTkLabel(self.dailybox, image=dailybox_logo, text="")
        daily_label2 = ctk.CTkLabel(self.dailybox, text="Today's Workout", font=("Roboto", 14), text_color="red")

        self.daily_label.image = dailybox_logo
        self.daily_label.place(x=2, y=0)
        daily_label2.place(x=40, y=10)

