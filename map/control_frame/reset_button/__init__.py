import tkinter as tk


class ResetButton(tk.Button):
    def __init__(self, board, *args, **kwargs):
        from wfc import Board
        board: Board

        super().__init__(*args, text='Reset', **kwargs)

        self.board = board
        self.bind('<Button-1>', self.handle_click)

    def handle_click(self, e: tk.Event):
        self.board.reset_board()
