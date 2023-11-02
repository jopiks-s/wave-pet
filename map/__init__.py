from tkinter import Misc

import customtkinter as ctk

from wfc import TileSet
from .board_frame import BoardFrame
from .control_frame import ControlFrame
from .speed_frame import SpeedFrame


class Map(ctk.CTkFrame):
    def __init__(self, master: Misc, tile_set_path: str, board_dimension: int, width: int, height: int):
        super().__init__(master, width, height, border_width=0)
        self.map_size = (width, height)

        self.tile_set = TileSet(tile_set_path)

        self.board_frm = BoardFrame(self, self.tile_set, board_dimension, 500, 4)  # magic_number
        self.control_frm = ControlFrame(self, self.board_frm.board, 600, 100, 10)  # magic_number
        self.speed_frm = SpeedFrame(width=600, height=100, internal_padx=10, master=self)  # magic_number

        self.board_frm.pack(anchor='center', pady=(10, 5))
        self.control_frm.pack(anchor='center', padx=10)
        self.speed_frm.pack(anchor='center', padx=10, pady=5)
