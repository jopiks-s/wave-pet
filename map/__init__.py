import customtkinter as ctk

from wfc import TileSet
from .board_frame import BoardFrame
from .control_frame import ControlFrame
from .speed_frame import SpeedFrame


class Map(ctk.CTkFrame):
    def __init__(self, board_dimension: int, tile_set_path: str, *args, **kwargs):
        assert 'width' in kwargs and 'height' in kwargs, 'Width and Height arguments not passed for initialization'

        super().__init__(*args, border_width=0, **kwargs)
        width, height = kwargs['width'], kwargs['height']
        self.map_size = (width, height)

        self.tile_set = TileSet(tile_set_path)

        self.board_frm = BoardFrame(self.tile_set, width=500, height=500, border_width=4,
                                    board_dimension=board_dimension, master=self)  # magic_number
        self.control_frm = ControlFrame(self.board_frm.board, width=600, height=100,
                                        master=self)  # magic_number
        self.speed_frm = SpeedFrame(width=600, height=100, master=self)  # magic_number

        self.board_frm.pack(anchor='center', pady=(10, 5))
        self.control_frm.pack(anchor='center', padx=10)
        self.speed_frm.pack(anchor='center', padx=10, pady=5)
