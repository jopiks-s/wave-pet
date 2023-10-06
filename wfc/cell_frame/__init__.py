import tkinter as tk

from wfc import ImageLabel


class CellFrame(tk.Frame):
    from ._actions import collapse_cell, update_cell
    from ._image_controller import delete_images, reorganize_layout

    def __init__(self, tile_set, size: int, *args, **kwargs):
        from wfc import TileSet, Tile

        super().__init__(*args, borderwidth=0, bg='black', **kwargs)
        self.grid_propagate(False)

        self.tile_set: TileSet = tile_set
        self.mapped_imgs: dict[tk.Label, Tile] = {}

        self._init_from_tile_set(size)

    def _init_from_tile_set(self, size: int):
        tile_set = self.tile_set

        img_size = int(size / tile_set.board_dim)
        scaled_imgs = tile_set.resize_pack(img_size)

        for i, tile in enumerate(tile_set.values()):
            row, col = i // tile_set.board_dim, i % tile_set.board_dim
            self.rowconfigure(row, weight=1)
            self.columnconfigure(col, weight=1)

            img_lbl = ImageLabel(tile.image, *scaled_imgs[tile.name],
                                 master=self, image=scaled_imgs[tile.name][1])
            img_lbl.grid(row=row, column=col, sticky='nsew')
            self.mapped_imgs[img_lbl] = tile
