import tkinter as tk
from tkinter import ttk


class ResolutionFrame(tk.Frame):
    def __init__(self, width, height, *args, **kwargs):
        super().__init__(*args, borderwidth=0, bg='orange', width=width, height=height, **kwargs)

        self.grid_propagate(False)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)

        self.progress_bar = ttk.Progressbar(value=50, master=self)
        self.progress_lbl = tk.Label(text='50/100', master=self)

        self.progress_bar.grid(row=0, column=0, sticky='nsew', padx=10, pady=35)  # magic_number
        self.progress_lbl.grid(row=0, column=1, sticky='w')
