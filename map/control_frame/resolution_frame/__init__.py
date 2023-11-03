import tkinter as tk

import customtkinter as ctk


class ResolutionFrame(ctk.CTkFrame):
    def __init__(self, master: tk.Misc, board, width: int, height: int):
        from wfc import Board
        board: Board

        super().__init__(master, width, height, fg_color='transparent', border_width=0, corner_radius=0)

        self.grid_propagate(False)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)

        self.board = board
        self.progress_txt = tk.StringVar(value=f'{board.solved.get()}/{board.real_size.get()}')

        self.progress_bar = ctk.CTkProgressBar(self, height=10)
        self.progress_bar.set(0)
        self.progress_color = '#1F6AA5'
        self.complete_color = 'green'

        self.progress_lbl = ctk.CTkLabel(text='50/100', textvariable=self.progress_txt, master=self)

        self.progress_bar.grid(row=0, column=0, sticky='we', padx=(5, 10))
        self.progress_lbl.grid(row=0, column=1, sticky='w')

        self.board.solved.trace_add('write', self._on_progress_change)
        self.board.real_size.trace_add('write', self._on_progress_change)
        self.board.complete.trace_add('write', self._on_state_change)

    def _on_progress_change(self, var, index, mode):
        solved = self.board.solved.get()
        real_size = self.board.real_size.get()
        out_txt = f'{solved}/{real_size}'

        diff = self.board.size - real_size
        if diff > 0:
            out_txt += f'({-diff})'

        self.progress_txt.set(out_txt)

        self.progress_bar.set(solved / real_size)

    def _on_state_change(self, var, index, mode):
        complete = self.board.complete.get()
        if complete:
            self.progress_bar.configure(progress_color=self.complete_color)
        else:
            self.progress_bar.configure(progress_color=self.progress_color)
