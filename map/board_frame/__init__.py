import tkinter as tk


class BoardFrame(tk.Frame):
    def __init__(self, width: int, height: int, board_dimension, cell_size, *args, **kwargs):
        assert width == height, 'Aspect ratio for BoardFrame not equal to 1.0 is not supported'

        super().__init__(*args, borderwidth=0, width=width, height=height, **kwargs)
        self.grid_propagate(False)
        self.rowconfigure(tuple(range(board_dimension)), weight=1, minsize=cell_size)
        self.columnconfigure(tuple(range(board_dimension)), weight=1, minsize=cell_size)
