import tkinter as tk

from PIL.Image import Image
from PIL.ImageTk import PhotoImage

from wfc import ImageLabel


class CellFrame(tk.Frame):
    from ._actions import collapse_cell, apply_new_rules, get_available_neighbors, get_entropy
    from ._image_controller import handle_image_click, select_image, delete_images, \
        _reorganize_layout, _update_image_size, _fill_empty_cell
    from ._state import State

    def __init__(self, board, tile_set, cell_size: int,
                 scaled_imgs: dict[str, Image], *args, **kwargs):
        from wfc import Tile, TileSet, Board
        board: Board
        tile_set: TileSet

        super().__init__(*args, borderwidth=2, relief='ridge', bg='black', **kwargs)

        self.grid_propagate(False)

        self.board = board
        self.tile_set = tile_set
        self.max_side = self.tile_set.get_square_bound()
        self.img_size = int(cell_size / self.max_side)
        self.mapped_imgs: dict[ImageLabel, Tile] = {}
        self.row = -1
        self.column = -1
        self.state = CellFrame.State.Stable

        self._init_from_tile_set(scaled_imgs)

    def _init_from_tile_set(self, scaled_imgs):
        for i, tile in enumerate(self.tile_set.values()):
            row, col = i // self.max_side, i % self.max_side
            img_lbl = ImageLabel(tile.image, scaled_imgs[tile.name], master=self)
            img_lbl.grid(row=row, column=col, sticky='nsew')
            img_lbl.bind('<Button-1>', self.handle_image_click)
            self.mapped_imgs[img_lbl] = tile

    def grid(self, **kwargs):
        if 'row' in kwargs:
            self.row = kwargs['row']
        if 'column' in kwargs:
            self.column = kwargs['column']

        super().grid(**kwargs)
