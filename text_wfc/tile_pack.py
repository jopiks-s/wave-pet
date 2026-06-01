from collections import UserDict
from typing import Any

from abc_wfc import AbcTilePack, Directions
from text_wfc.tile import TextTile


class TextTilePack(AbcTilePack, UserDict[str, TextTile]):
    def load_tile(self, tile_name: str, content: list[Any]) -> TextTile:
        allowed_tiles, symbol, style = content
        allowed_tiles = {Directions[_dir]: set(tiles) for _dir, tiles in allowed_tiles.items()}
        return TextTile(tile_name, allowed_tiles, symbol, style)
