import json
import os

import customtkinter as ctk
from PIL import Image

from .tile import Tile


class TileSet:
    from ._tile_pack import __len__, items, values, resize_pack, get_square_bound

    def __init__(self, path: str):
        rules_path = f'{path}/set_rules.json'
        assert os.path.exists(rules_path), f'Path to rules file: {rules_path}'

        self.tile_pack: dict[str, Tile] = {}
        with open(rules_path, 'r') as f:
            set_rules = json.load(f)
            for file_name in os.listdir(path):
                if file_name.split('.')[1] not in ('png', 'jpg'):
                    continue

                name = file_name.split('.')[0]
                img = Image.open(f'{path}/{file_name}')
                image = ctk.CTkImage(img, size=img.size)
                self.tile_pack[name] = Tile(name, set_rules[name], image)
