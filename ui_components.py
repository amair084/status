import customtkinter as ctk
import tkinter as tk

def _get_scrollable_parent(scrollable):
    for name in ("scrollable_frame", "frame", "inner_frame", "_frame", "_inner_frame"):
        if hasattr(scrollable, name):
            return getattr(scrollable, name)

    for child in scrollable.winfo_children():
        if isinstance(child, (ctk.CTkFrame, tk.Frame)):
            return child

    return scrollable

def clone_day_box(self, day_index):
    original_box = self.day_boxes[day_index]

    cloned_box = ctk.CTkFrame(
        self.dailybox,
        fg_color=original_box.cget("fg_color"),
        width=original_box.winfo_width(),
        height=original_box.winfo_height(),
        corner_radius=original_box.cget("corner_radius") if hasattr(original_box, "cget") else 8
    )
    cloned_box.place(x=10, y=10)

    for child in original_box.winfo_children():

        if isinstance(child, ctk.CTkLabel):
            new_label = ctk.CTkLabel(
                cloned_box,
                text=child.cget("text"),
                font=child.cget("font"),
                fg_color=child.cget("fg_color") if "fg_color" in child.keys() else None,
                height=child.winfo_height()
            )
            new_label.pack(anchor="nw", side="top", fill="x", expand=False, pady=5, padx=3)


    return cloned_box