import tkinter as tk
from tkinter import ttk


class ResolutionFrame(tk.Frame):
    def __init__(self, board, width: int, height: int, *args, **kwargs):
        from wfc import Board
        board: Board

        super().__init__(*args, borderwidth=0, bg='orange', width=width, height=height, **kwargs)

        self.grid_propagate(False)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)

        self.board = board
        self.progress_txt = tk.StringVar(value=f'{board.complete.get()}/{board.real_size.get()}')

        self.progress_bar = ttk.Progressbar(value=0, variable=board.complete, master=self)
        self.progress_lbl = tk.Label(text='50/100', textvariable=self.progress_txt, master=self)

        self.progress_bar.grid(row=0, column=0, sticky='nsew', padx=10, pady=35)  # magic_number
        self.progress_lbl.grid(row=0, column=1, sticky='w')

        self.board.complete.trace_add('write', self._on_complete_change)
        self.board.real_size.trace_add('write', self._on_complete_change)

    def _on_complete_change(self, var, index, mode):
        complete = self.board.complete.get()
        real_size = self.board.real_size.get()
        out_txt = f'{complete}/{real_size}'

        diff = self.board.size - real_size
        if diff > 0:
            out_txt += f'({-diff})'

        self.progress_txt.set(out_txt)

        self.progress_bar['maximum'] = real_size
