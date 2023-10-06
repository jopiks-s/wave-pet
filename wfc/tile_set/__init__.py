import json
import math
import os

from PIL import ImageTk, Image


class Tile:
    def __init__(self, name: str, rules: list[list[str]], img: Image.Image):
        self.name = name
        self.rules = rules
        self.image = img


class TileSet:
    def __init__(self, path: str, map_frm, map_size: int, cell_size: int):
        from wfc import CellFrame
        from map import Map
        map_frm: Map

        rules_path = f'{path}/set_rules.json'
        assert os.path.exists(rules_path), f'Path to rules file: {rules_path}'

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

        self.board_dim = math.ceil(math.sqrt(len(self.tile_pack)))
        self.grid_size = (math.ceil(len(self) / self.board_dim),
                          self.board_dim)

        self._create_map(map_frm, map_size, cell_size)

    def _create_map(self, map_frm, map_size, cell_size):
        from wfc import CellFrame

        for i in range(map_size):
            self.board.append([])
            for j in range(map_size):
                cell_frm = CellFrame(self, cell_size, master=map_frm)
                cell_frm.grid(row=i, column=j, sticky='nsew')
                self.board[i].append(cell_frm)

    def __len__(self):
        return len(self.tile_pack)

    def items(self):
        return self.tile_pack.items()

    def values(self):
        return self.tile_pack.values()

    def resize_pack(self, size: int) -> dict[str, tuple[Image.Image, ImageTk.PhotoImage]]:
        scaled_imgs = {}
        for name, tile in self.items():
            resized_img = tile.image.resize((size, size), Image.LANCZOS)
            scaled_imgs[name] = (resized_img, ImageTk.PhotoImage(resized_img))

        return scaled_imgs

    def propagate_collapse(self, row, column):
        ...
