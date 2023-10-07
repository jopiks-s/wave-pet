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
