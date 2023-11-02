import customtkinter as ctk


class BoardFrame(ctk.CTkFrame):
    def __init__(self, tile_set, width: int, height: int, border_width: int, board_dimension: int, *args, **kwargs):
        from wfc import TileSet, Board
        tile_set: TileSet

        assert width == height, 'Aspect ratio for BoardFrame not equal to 1.0 is not supported'

        super().__init__(*args, border_width=0, width=width, height=height,
                         **kwargs)
        self.grid_propagate(False)

        # formula to get the cell size of the divisible without remainder by the number of cells
        self.cell_size = width - border_width * 2
        self.to_pady = self.to_padx = self.cell_size % board_dimension + border_width * 2
        self.cell_size = int((self.cell_size - self.to_padx) / board_dimension)

        self.board = Board(board_dimension, tile_set, self)
