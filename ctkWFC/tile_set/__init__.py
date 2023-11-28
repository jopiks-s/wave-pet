import json
import os

from PIL import Image
from customtkinter import CTkImage

from AbstractWFC import tile_set
from AbstractWFC.tile import Directions

from ctkWFC.tile import Tile


class TileSet(tile_set.TileSet):
    def load(self, folder: str):
        rules_path = f'{folder}/{TileSet.rules_file_name}'
        assert os.path.exists(rules_path), f'Rules file doesn`t exist: {rules_path}'

        with open(rules_path, 'r') as f:
            rule_set = json.load(f)
            tile_imgs = {name.split('.')[0]: name for name in os.listdir(folder) if
                         name.split('.')[-1] in ('png', 'jpg')}
            for tile_name, rules in rule_set.items():
                assert tile_name in tile_imgs, f'Tile "{tile_name}" does not have image in: {folder}'
                rules = {Directions[direction]: valid_neighbors for direction, valid_neighbors in rules.items()}
                image = Image.open(f'{folder}/{tile_imgs[tile_name]}')
                image = CTkImage(image, size=image.size)
                self.__setitem__(tile_name, Tile(tile_name, rules, image))


    def set_size(self, size):
        for tile in self.values():
            tile.image.configure(size=(size, size))
