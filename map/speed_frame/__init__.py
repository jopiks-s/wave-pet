import tkinter as tk
from tkinter import ttk


class SpeedFrame(tk.Frame):
    def __init__(self, width, height, *args, **kwargs):
        super().__init__(*args, borderwidth=0, bg='cyan', width=width, height=height, **kwargs)

        self.grid_propagate(False)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)

        self.speed_slide = ttk.Scale(from_=1, to=5, value=1, master=self)
        self.speed_lbl = tk.Label(text='1x', master=self)

        self.speed_slide.grid(row=0, column=0, padx=10, pady=35, sticky='nsew')  # magic_number
        self.speed_lbl.grid(row=0, column=1, sticky='w')
