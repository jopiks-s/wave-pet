import tkinter as tk

from wfc import TileSet


class Map(tk.Frame):
    def __init__(self, map_size: int, tile_set_path: str, *args, **kwargs):
        assert 'width' in kwargs and 'height' in kwargs, 'Width and Height arguments not passed for initialization'

        super().__init__(*args, borderwidth=0, **kwargs)
        self.grid_propagate(False)

        cell_size = min(kwargs['width'], kwargs['height']) / map_size
        self.map_size = map_size
        self.tile_set = TileSet(tile_set_path, self, map_size, cell_size)

        self.rowconfigure(tuple(range(map_size)), weight=1, minsize=cell_size)
        self.columnconfigure(tuple(range(map_size)), weight=1, minsize=cell_size)
