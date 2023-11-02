from tkinter import Misc

import customtkinter as ctk

from .reset_button import ResetButton
from .resolution_frame import ResolutionFrame
from .solve_button import SolveButton


class ControlFrame(ctk.CTkFrame):
    def __init__(self, master: Misc, board, width: int, height: int, internal_padx: int):
        super().__init__(master, width, height, border_width=0)

        self.grid_propagate(False)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=5)
        self.columnconfigure([1, 2], weight=1)

        self.resolution_frame = ResolutionFrame(self, board, 100, 100)  # magic_number
        self.reset_btn = ResetButton(self, board)
        self.solve_btn = SolveButton(self, board)

        self.resolution_frame.grid(row=0, column=0, sticky='we', padx=(internal_padx, 0))
        self.reset_btn.grid(row=0, column=1, sticky='we', padx=3)
        self.solve_btn.grid(row=0, column=2, sticky='we', padx=(3, internal_padx))
