import tkinter as tk


class ResetButton(tk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, text='Reset', **kwargs)
