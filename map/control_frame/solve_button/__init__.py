import tkinter as tk


class SolveButton(tk.Button):
    def __init__(self, tile_set, *args, **kwargs):
        from wfc import TileSet
        tile_set: TileSet
        super().__init__(*args, text='Solve', **kwargs)

        self.tile_set = tile_set
        self.bind('<Button-1>', self.handle_click)

    def handle_click(self, e: tk.Event):
        self.tile_set.auto_solve()
