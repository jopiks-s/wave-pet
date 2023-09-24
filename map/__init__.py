import tkinter as tk

from wfc import TileSet, create_map_layout


class Map(tk.Frame):
    def __init__(self, map_size: int, cell_size: int, tile_set_path: str, *args, **kwargs):
        super().__init__(borderwidth=0, *args, **kwargs)
        self.map_size = map_size
        self.tile_set = TileSet(tile_set_path)

        self.rowconfigure(tuple(range(map_size)), weight=1, minsize=cell_size)
        self.columnconfigure(tuple(range(map_size)), weight=1, minsize=cell_size)
        self.grid_propagate(False)

        create_map_layout(self, self.tile_set, map_size, cell_size)
