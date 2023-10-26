import tkinter as tk


class BoardFrame(tk.Frame):
    def __init__(self, tile_set, width: int, height: int, board_dimension: int, *args, **kwargs):
        from wfc import TileSet, Board
        tile_set: TileSet

        assert width == height, 'Aspect ratio for BoardFrame not equal to 1.0 is not supported'

        super().__init__(*args, borderwidth=0, width=width, height=height, **kwargs)

        self.cell_size = min(width, height) / board_dimension

        self.grid_propagate(False)
        self.rowconfigure(tuple(range(board_dimension)), weight=1, minsize=self.cell_size)
        self.columnconfigure(tuple(range(board_dimension)), weight=1, minsize=self.cell_size)

        self.board = Board(board_dimension, tile_set, self)
