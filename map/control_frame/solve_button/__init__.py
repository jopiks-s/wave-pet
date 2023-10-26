import tkinter as tk


class SolveButton(tk.Button):
    def __init__(self, board, tile_set, *args, **kwargs):
        from wfc import TileSet, Board
        board: Board
        tile_set: TileSet
        super().__init__(*args, text='Solve', **kwargs)

        self.board = board
        self.tile_set = tile_set
        self.bind('<Button-1>', self.handle_click)

    def handle_click(self, e: tk.Event):
        self.board.auto_solve()
