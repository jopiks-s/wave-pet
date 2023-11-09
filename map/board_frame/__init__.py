from tkinter import Misc

import customtkinter as ctk

from ._on_complete import on_complete_impulse_animation


class BoardFrame(ctk.CTkFrame):
    def __init__(self, master: Misc, tile_set, board_dimension: int, size: int, border_width: int):
        from wfc import TileSet, Board
        tile_set: TileSet

        super().__init__(master, size, size, border_width=0, border_color='green')
        self.grid_propagate(False)

        self.border_width = border_width
        # formula to get the cell size of the divisible without remainder by the number of cells
        self.cell_size = size - border_width * 2
        self.to_pady = self.to_padx = self.cell_size % board_dimension + border_width * 2
        self.cell_size = int((self.cell_size - self.to_padx) / board_dimension)

        self.board = Board(board_dimension, tile_set, self)

        self.board.complete.trace_add('write', self._on_complete_change)

    def _on_complete_change(self, var, index, mode):
        if self.board.complete.get():
            on_complete_impulse_animation(self, 2, 30, 100, 'green')
        else:
            on_complete_impulse_animation(self, 1, 60, 0, 'gray')
