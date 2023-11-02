import tkinter as tk

import customtkinter as ctk


class SolveButton(ctk.CTkButton):
    def __init__(self, master: tk.Misc, board):
        from wfc import TileSet, Board
        board: Board
        tile_set: TileSet

        super().__init__(master, 0, 30, text='Solve')

        self.board = board
        self.bind('<Button-1>', self.handle_click)

    def handle_click(self, e: tk.Event):
        self.board.auto_solve()
