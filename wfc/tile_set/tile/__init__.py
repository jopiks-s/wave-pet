from dataclasses import dataclass, field
from enum import Enum

from PIL import Image


class Tile:
    class Directions(Enum):
        UP = 'UP'
        RIGHT = 'RIGHT'
        DOWN = 'DOWN'
        LEFT = 'LEFT'

    def __init__(self, name: str, rules: list[list[str]], img: Image.Image):
        self.name = name
        self.rules = rules
        self.image = img


@dataclass
class AvailableNeighbors:
    UP: list[str] = field(default_factory=lambda: [])
    RIGHT: list[str] = field(default_factory=lambda: [])
    DOWN: list[str] = field(default_factory=lambda: [])
    LEFT: list[str] = field(default_factory=lambda: [])

    def __getitem__(self, item: Tile.Directions):
        assert isinstance(item, Tile.Directions), \
            'Only the enumeration keys from "Tile.Directions" are available for accessing attributes'

        return self.__getattribute__(item.name)

    def __setitem__(self, key, value):
        assert isinstance(key, Tile.Directions), \
            'Only the enumeration keys from "Tile.Directions" are available for accessing attributes'

        self.__setattr__(key.name, value)
