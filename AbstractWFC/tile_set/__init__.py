import json
import os
from collections import UserDict
from copy import deepcopy
from math import ceil, sqrt

from AbstractWFC import tile
from AbstractWFC.tile import Tile


class TileSet(UserDict):
    rules_file_name = 'rule_set.json'

    def __init__(self, folder: str):
        super().__init__()

        self._square_bound: int = 0
        self.load(folder)

    def load(self, folder: str):
        rules_path = f'{folder}/{TileSet.rules_file_name}'
        assert os.path.exists(rules_path), f'Rules file doesn`t exist: {rules_path}'

        with open(rules_path, 'r') as f:
            rule_set = json.load(f)
            for tile_name, rules in rule_set.items():
                rules = {tile.Directions[direction]: valid_neighbors for direction, valid_neighbors in rules.items()}
                self.__setitem__(tile_name, Tile(tile_name, rules))

    @property
    def square_bound(self) -> int:
        if self._square_bound == 0:
            self._square_bound = ceil(sqrt(len(self)))

        return self._square_bound

    def deepcopy(self) -> dict[str, Tile]:
        return deepcopy(self.data)
    def __setitem__(self, key: str, value: Tile):
        assert key not in self, 'Attempt to reassign existing tile'
        self._square_bound = 0
        super().__setitem__(key, value)

    def clear(self):
        self._square_bound = 0
        super().clear()
