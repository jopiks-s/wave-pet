import json
import math
import os

from PIL import Image

from .tile import Tile


class TileSet:
    from ._entropy import propagate_collapse, auto_solve
    from ._tile_pack import __len__, items, values, resize_pack, get_coords

    def __init__(self, path: str, map_frm, map_size: int, cell_size: int):
        from wfc import CellFrame
        from map import Map

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

        self._create_map(map_frm, map_size, cell_size)

    def _create_map(self, map_frm, map_size, cell_size):
        from wfc import CellFrame

        scaled_imgs = self.resize_pack(int(cell_size / self.cell_dim))
        for i in range(map_size):
            self.board.append([])
            for j in range(map_size):
                cell_frm = CellFrame(self, cell_size, scaled_imgs, master=map_frm)
                cell_frm.grid(row=i, column=j, sticky='nsew')
                self.board[i].append(cell_frm)
