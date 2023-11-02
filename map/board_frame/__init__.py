from tkinter import Misc

import customtkinter as ctk


class BoardFrame(ctk.CTkFrame):
    def __init__(self, master: Misc, tile_set, board_dimension: int, size: int, border_width: int):
        from wfc import TileSet, Board
        tile_set: TileSet

        super().__init__(master, size, size, border_width=0)
        self.grid_propagate(False)

        # formula to get the cell size of the divisible without remainder by the number of cells
        self.cell_size = size - border_width * 2
        self.to_pady = self.to_padx = self.cell_size % board_dimension + border_width * 2
        self.cell_size = int((self.cell_size - self.to_padx) / board_dimension)

        self.board = Board(board_dimension, tile_set, self)
