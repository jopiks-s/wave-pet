import customtkinter as ctk
from dataclasses import dataclass, field
from enum import Enum

from PIL import Image


@dataclass(frozen=True)
class Tile:
    class Directions(Enum):
        UP = 'UP'
        RIGHT = 'RIGHT'
        DOWN = 'DOWN'
        LEFT = 'LEFT'

    name: str
    rules: list[list[str]]
    image: ctk.CTkImage


@dataclass
class AvailableNeighbors:
    UP: list[str] = field(default_factory=lambda: [])
    RIGHT: list[str] = field(default_factory=lambda: [])
    DOWN: list[str] = field(default_factory=lambda: [])
    LEFT: list[str] = field(default_factory=lambda: [])

    def __getitem__(self, item: Tile.Directions) -> list[str]:
        assert isinstance(item, Tile.Directions), \
            'Only the enumeration keys from "Tile.Directions" are available for accessing attributes'

        return self.__getattribute__(item.name)

    def __setitem__(self, key, value) -> None:
        assert isinstance(key, Tile.Directions), \
            'Only the enumeration keys from "Tile.Directions" are available for accessing attributes'

        self.__setattr__(key.name, value)
