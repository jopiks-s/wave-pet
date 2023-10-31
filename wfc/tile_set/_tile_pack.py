from copy import copy
from math import ceil, sqrt
from typing import TypeVar, ValuesView

from PIL import Image, ImageTk
import customtkinter as ctk


def __len__(self) -> int:
    from . import TileSet
    self: TileSet

    return len(self.tile_pack)


def items(self):
    from . import TileSet
    self: TileSet

    return self.tile_pack.items()


Tile = TypeVar('Tile')


def values(self) -> ValuesView[Tile]:
    from . import TileSet
    self: TileSet

    return self.tile_pack.values()


def resize_pack(self, size: int) -> dict[str, ctk.CTkImage]:
    scaled_imgs = {}
    for name, tile in self.items():
        resize_image: ctk.CTkImage = copy(tile.image)
        resize_image.configure(size=(size, size))
        scaled_imgs[name] = resize_image

    return scaled_imgs


def get_square_bound(self):
    from . import TileSet
    self: TileSet

    return ceil(sqrt(len(self)))
