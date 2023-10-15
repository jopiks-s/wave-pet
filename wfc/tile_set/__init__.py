import json
import math
import os

from PIL import Image

from .tile import Tile


class TileSet:
    from ._entropy import propagate_collapse, auto_solve
    from ._tile_pack import __len__, items, values, resize_pack, get_coords
    from ._initialize_board import _create_board

    def __init__(self, path: str, map_frm, board_frm):
        from wfc import CellFrame
        from map import Map, BoardFrame
        map_frm: Map
        board_frm: BoardFrame

        rules_path = f'{path}/set_rules.json'
        assert os.path.exists(rules_path), f'Path to rules file: {rules_path}'

        self.map_frm: Map = map_frm
        self.board: list[list[CellFrame]] = []
        self.tile_pack = {}
        with open(rules_path, 'r') as f:
            set_rules = json.load(f)
            for file_name in os.listdir(path):
                if file_name.split('.')[1] not in ('png', 'jpg'):
                    continue

                name = file_name.split('.')[0]
                img = Image.open(f'{path}/{file_name}')
                self.tile_pack[name] = Tile(name, set_rules[name], img)

        self.cell_dim = math.ceil(math.sqrt(len(self.tile_pack)))
        self.grid_size = (math.ceil(len(self) / self.cell_dim),
                          self.cell_dim)

        self._create_board(map_frm, board_frm)
