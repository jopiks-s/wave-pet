import tkinter as tk

from wfc import TileSet
from .board_frame import BoardFrame
from .control_frame import ControlFrame
from .speed_frame import SpeedFrame


class Map(tk.Frame):
    def __init__(self, board_dimension: int, tile_set_path: str, *args, **kwargs):
        assert 'width' in kwargs and 'height' in kwargs, 'Width and Height arguments not passed for initialization'

        super().__init__(*args, borderwidth=0, **kwargs)
        width, height = kwargs['width'], kwargs['height']
        self.map_size = (width, height)

        self.tile_set = TileSet(tile_set_path)

        self.board_frm = BoardFrame(self.tile_set, width=500, height=500, board_dimension=board_dimension,
                                    master=self)  # magic_number
        self.control_frm = ControlFrame(self.board_frm.board, self.tile_set, width=500, height=100,
                                        master=self)  # magic_number
        self.speed_frm = SpeedFrame(width=500, height=100, master=self)  # magic_number

        self.board_frm.pack(anchor='center')
        self.control_frm.pack(anchor='center')
        self.speed_frm.pack(anchor='center')
