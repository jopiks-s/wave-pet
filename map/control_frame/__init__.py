import tkinter as tk

from .resolution_frame import ResolutionFrame
from .solve_button import SolveButton
from .reset_button import ResetButton


class ControlFrame(tk.Frame):
    def __init__(self, board, width: int, height: int, *args, **kwargs):
        super().__init__(*args, borderwidth=0, bg='purple', width=width, height=height, **kwargs)

        self.grid_propagate(False)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=3)
        self.columnconfigure([1, 2], weight=1)

        self.resolution_frame = ResolutionFrame(board, 100, 100, master=self)  # magic_number
        self.reset_btn = ResetButton(board, master=self)
        self.solve_btn = SolveButton(board, master=self)

        self.resolution_frame.grid(row=0, column=0, sticky='nsew')
        self.reset_btn.grid(row=0, column=1, sticky='we', padx=5, ipady=8)  # magic_number
        self.solve_btn.grid(row=0, column=2, sticky='we', padx=5, ipady=8)  # magic_number
