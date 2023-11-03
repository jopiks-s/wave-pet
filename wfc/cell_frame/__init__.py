from copy import copy
from tkinter import Misc

import customtkinter as ctk

from wfc import ImageLabel


class CellFrame(ctk.CTkFrame):
    from ._actions import reset_cell, collapse_cell, apply_new_rules, get_available_neighbors, get_entropy
    from ._image_controller import image_click_handler, _select_image, _delete_images, _delete_all_images, \
        _reorganize_layout, _update_image_size, _fill_empty_cell, _undo_fill_empty_cell
    from ._state import State

    def __init__(self, master: Misc, board, tile_set, scaled_imgs: dict[str, ctk.CTkImage], size: int):
        from wfc import Tile, TileSet, Board
        board: Board
        tile_set: TileSet

        super().__init__(master, size, size, 0, 0, fg_color='transparent')

        self.grid_propagate(False)

        self.board = board
        self.tile_set = tile_set

        self.max_side = self.tile_set.get_square_bound()
        self.cell_size = size
        self.img_size = int(self.cell_size / self.max_side)
        self.mapped_imgs: dict[ImageLabel, Tile] = {}
        self.imgs_copy: dict[ImageLabel, Tile] = {}
        self.row = -1
        self.column = -1
        self.state: CellFrame.State | None = None

        self.create_from_tile_set(scaled_imgs)

    def create_from_tile_set(self, scaled_imgs: dict[str, ctk.CTkImage] | None = None):
        if not self.imgs_copy:
            assert scaled_imgs is not None, 'Can`t create CellFrame without scaled_imgs'
            for i, tile in enumerate(self.tile_set.values()):
                row, col = i // self.max_side, i % self.max_side
                img_lbl = ImageLabel(self, self.img_size, copy(scaled_imgs[tile.name]))
                img_lbl.grid(row=row, column=col, sticky='nsew')
                img_lbl.bind('<Button-1>', self.image_click_handler)
                self.mapped_imgs[img_lbl] = tile

            self.state = CellFrame.State.Stable
            self.imgs_copy = self.mapped_imgs.copy()
        else:
            self.mapped_imgs = self.imgs_copy.copy()
            self._reorganize_layout()

    def grid(self, **kwargs):
        if 'row' in kwargs:
            self.row = kwargs['row']
        if 'column' in kwargs:
            self.column = kwargs['column']

        super().grid(**kwargs)
