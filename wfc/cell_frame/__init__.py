from random import choice
import tkinter as tk

from wfc import ImageLabel


class CellFrame(tk.Frame):
    from ._actions import collapse_cell, update_cell
    from ._image_controller import delete_images, reorganize_layout, update_image_size

    def __init__(self, tile_set, size: int, *args, **kwargs):
        from wfc import TileSet, Tile

        super().__init__(*args, borderwidth=0, bg='black', **kwargs)
        self.grid_propagate(False)

        self.tile_set: TileSet = tile_set
        self.max_side = self.tile_set.board_dim
        self.img_size = int(size / self.max_side)
        self.mapped_imgs: dict[ImageLabel, Tile] = {}

        self._init_from_tile_set(size)

    def _init_from_tile_set(self, size: int):
        tile_set = self.tile_set

        scaled_imgs = tile_set.resize_pack(self.img_size)

        for i, tile in enumerate(tile_set.values()):
            row, col = i // tile_set.board_dim, i % tile_set.board_dim
            img_lbl = ImageLabel(tile.image, *scaled_imgs[tile.name],
                                 master=self, image=scaled_imgs[tile.name][1])
            img_lbl.grid(row=row, column=col, sticky='nsew')
            self.mapped_imgs[img_lbl] = tile
