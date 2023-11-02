import customtkinter as ctk

from .reset_button import ResetButton
from .resolution_frame import ResolutionFrame
from .solve_button import SolveButton


class ControlFrame(ctk.CTkFrame):
    def __init__(self, board, width: int, height: int, *args, **kwargs):
        super().__init__(*args, border_width=0, width=width, height=height, **kwargs)

        self.grid_propagate(False)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=5)
        self.columnconfigure([1, 2], weight=1)

        self.resolution_frame = ResolutionFrame(board, 100, 100, master=self)  # magic_number
        self.reset_btn = ResetButton(board, master=self)
        self.solve_btn = SolveButton(board, master=self)

        self.resolution_frame.grid(row=0, column=0, sticky='we', padx=(10, 0))
        self.reset_btn.grid(row=0, column=1, sticky='we', padx=3)  # magic_number
        self.solve_btn.grid(row=0, column=2, sticky='we', padx=(3, 10))  # magic_number
