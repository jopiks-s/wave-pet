import tkinter as tk

from wfc import TileSet
from .board_frame import BoardFrame
from .control_frame import ControlFrame


class Map(tk.Frame):
    def __init__(self, board_dimension: int, tile_set_path: str, *args, **kwargs):
        assert 'width' in kwargs and 'height' in kwargs, 'Width and Height arguments not passed for initialization'

        super().__init__(*args, borderwidth=0, **kwargs)

        self.board_dimension = board_dimension
        self.frm_size = {'width': kwargs['width'], 'height': kwargs['height']}
        self.board_size = {'width': kwargs['width'] - 100, 'height': kwargs['height'] - 200}  # magic_number
        self.cell_size = min(self.board_size['width'], self.board_size['height']) / board_dimension

        self.board_frm = BoardFrame(self.board_size['width'], self.board_size['height'],
                                    board_dimension, self.cell_size, master=self)
        self.tile_set = TileSet(tile_set_path, map_frm=self, board_frm=self.board_frm)
        self.control_frm = ControlFrame(width=500, height=100, master=self)  # magic_number

        self.board_frm.pack(anchor='center')
        self.control_frm.pack(anchor='center')
