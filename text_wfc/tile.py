from dataclasses import dataclass
from rich.text import Text

from abc_wfc import AbcTile, Directions


@dataclass(frozen=True)
class TextTile(AbcTile):
    name: str
    allowed_tiles: dict[Directions, set[str]]
    _symbol: str
    style: str

    def __str__(self) -> str:
        return self._symbol

    @property
    def symbol(self) -> Text:
        return Text(self._symbol, self.style)


    def __rich__(self) -> Text:
        return self.symbol
