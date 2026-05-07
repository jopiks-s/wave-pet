from dataclasses import dataclass

from abc_wfc import AbcTile, Directions


@dataclass(frozen=True)
class TextTile(AbcTile):
    name: str
    allowed_tiles: dict[Directions, set[str]]
    symbol: str

    def represent(self) -> str:
        return self.symbol
