import tkinter as tk

from PIL.Image import Image
from PIL.ImageTk import PhotoImage

from wfc import ImageLabel, TileSet


class CellFrame(tk.Frame):
    from ._actions import collapse_cell, apply_new_rules, get_available_neighbors, finish_cell
    from ._image_controller import select_image, delete_images, _reorganize_layout, _update_image_size, _fill_empty_cell

    def __init__(self, tile_set, size: int,
                 scaled_imgs: dict[str, tuple[Image, PhotoImage]] | None = None, *args, **kwargs):
        from wfc.tile_set import Tile

        super().__init__(*args, borderwidth=2, relief='ridge', bg='black', **kwargs)
        self.grid_propagate(False)

        self.tile_set: TileSet = tile_set
        self.max_side = self.tile_set.cell_dim
        self.img_size = int(size / self.max_side)
        self.mapped_imgs: dict[ImageLabel, Tile] = {}
        self.row = -1
        self.column = -1
        self.finish = False

        self._init_from_tile_set(size, scaled_imgs)

    def _init_from_tile_set(self, size, scaled_imgs):
        tile_set = self.tile_set
        if scaled_imgs is None:
            scaled_imgs = tile_set.resize_pack(self.img_size)

        for i, tile in enumerate(tile_set.values()):
            row, col = i // tile_set.cell_dim, i % tile_set.cell_dim
            img_lbl = ImageLabel(tile.image, *scaled_imgs[tile.name],
                                 master=self, image=scaled_imgs[tile.name][1])
            img_lbl.grid(row=row, column=col, sticky='nsew')
            img_lbl.bind('<Button-1>', self.collapse_cell)
            self.mapped_imgs[img_lbl] = tile

    def grid(self, **kwargs):
        if 'row' in kwargs:
            self.row = kwargs['row']
        if 'column' in kwargs:
            self.column = kwargs['column']

        super().grid(**kwargs)
