import tkinter as tk

from PIL.Image import Image

from wfc import ImageLabel


class CellFrame(tk.Frame):
    from ._actions import reset_cell, collapse_cell, apply_new_rules, get_available_neighbors, get_entropy
    from ._image_controller import handle_image_click, _select_image, _delete_images, _delete_all_images, \
        _reorganize_layout, _update_image_size, _fill_empty_cell, _undo_fill_empty_cell
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
        self.scaled_imgs = scaled_imgs

        self.max_side = self.tile_set.get_square_bound()
        self.img_size = int(cell_size / self.max_side)
        self.mapped_imgs: dict[ImageLabel, Tile] = {}
        self.imgs_copy: dict[ImageLabel, Tile] = {}
        self.row = -1
        self.column = -1
        self.state: CellFrame.State | None = None

        self.create_from_tile_set()

    def create_from_tile_set(self):
        if not self.imgs_copy:
            for i, tile in enumerate(self.tile_set.values()):
                row, col = i // self.max_side, i % self.max_side
                img_lbl = ImageLabel(tile.image, self.scaled_imgs[tile.name], master=self)
                img_lbl.grid(row=row, column=col, sticky='nsew')
                img_lbl.bind('<Button-1>', self.handle_image_click)
                self.mapped_imgs[img_lbl] = tile

            self.state = CellFrame.State.Stable
            self.imgs_copy = self.mapped_imgs.copy()
        else:
            for i, img_lbl in enumerate(self.imgs_copy):
                row, col = i // self.max_side, i % self.max_side
                img_lbl.grid(row=row, column=col, sticky='nsew')

            self.mapped_imgs = self.imgs_copy.copy()
            self._update_image_size()

    def grid(self, **kwargs):
        if 'row' in kwargs:
            self.row = kwargs['row']
        if 'column' in kwargs:
            self.column = kwargs['column']

        super().grid(**kwargs)
