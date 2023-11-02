import tkinter as tk

import customtkinter as ctk


class ResetButton(ctk.CTkButton):
    def __init__(self, master: tk.Misc, board):
        from wfc import Board
        board: Board

        super().__init__(master, 0, 30, text='Reset')

        self.board = board
        self.bind('<Button-1>', self.handle_click)

    def handle_click(self, e: tk.Event):
        self.board.reset_board()
