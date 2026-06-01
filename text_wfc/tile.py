from dataclasses import dataclass, field

from rich.text import Text

from abc_wfc import AbcTile, Directions


@dataclass(frozen=True)
class TextTile(AbcTile):
    name: str
    allowed_tiles: dict[Directions, set[str]]
    raw_symbol: str
    style: str
    symbol: Text = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "symbol", Text(self.raw_symbol, self.style))

    def __str__(self) -> str:
        return self.symbol

    def __rich__(self) -> Text:
        return self.symbol
