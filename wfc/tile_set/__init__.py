import json
import os
from collections import UserDict
from copy import copy
from math import ceil, sqrt

import customtkinter as ctk
from PIL import Image

from .tile import Tile

# todo add safe checker for 'rule_set'.
#  Unsafe situation example:
#  'up' tile with rules: {Direction.RIGHT: ["left", "down", "up"], ...} which allow 'left' tile.
#  'left' tile with rules: {Direction.LEFT: ["down", "right"], ...} which does not allow 'up' tile.
class TileSet(UserDict):
    rules_file_name = 'rule_set.json'

    def __init__(self, path: str):
        rules_path = f'{path}/{TileSet.rules_file_name}'
        assert os.path.exists(rules_path), f'Rules file doesn`t exist: {rules_path}'

        super().__init__()

        self._square_bound: int = 0
        with open(rules_path, 'r') as f:
            rule_set = json.load(f)
            for file_name in os.listdir(path):
                if file_name.split('.')[1] not in ('png', 'jpg'):
                    continue

                name = file_name.split('.')[0]
                rules = {Tile.Directions[direction]: valid_neighbors for direction, valid_neighbors in rule_set[name].items()}
                image = Image.open(f'{path}/{file_name}')
                image = ctk.CTkImage(image, size=image.size)
                super().__setitem__(name, Tile(name, rules, image))

    @property
    def square_bound(self) -> int:
        if self._square_bound == 0:
            self._square_bound = ceil(sqrt(len(self)))

        return self._square_bound

    def get_resized(self, size: int) -> dict[str, ctk.CTkImage]:
        scaled_imgs = {}
        for name, tile in self.items():
            resize_image: ctk.CTkImage = copy(tile.image)
            resize_image.configure(size=(size, size))
            scaled_imgs[name] = resize_image

        return scaled_imgs
