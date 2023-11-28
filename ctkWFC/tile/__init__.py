from customtkinter import CTkImage

from dataclasses import dataclass

from AbstractWFC import tile

@dataclass(frozen=True)
class Tile(tile.Tile):
    image: CTkImage
