from math import ceil, sqrt
from typing import TypeVar, ValuesView

from PIL import Image, ImageTk


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


def resize_pack(self, size: int) -> dict[str, Image.Image]:
    scaled_imgs = {}
    for name, tile in self.items():
        scaled_imgs[name] = tile.image.resize((size, size), Image.LANCZOS)

    return scaled_imgs


def get_square_bound(self):
    from . import TileSet
    self: TileSet

    return ceil(sqrt(len(self)))
