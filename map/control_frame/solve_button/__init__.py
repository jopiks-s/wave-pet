import tkinter as tk


class SolveButton(tk.Button):
    def __init__(self, tile_set, *args, **kwargs):
        super().__init__(*args, text='Solve', **kwargs)

        self.tile_set = tile_set
        self.bind('<Button-1>', self.a)

    def a(self, a):
        print('a')
