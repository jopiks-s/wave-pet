from dataclasses import dataclass

from .directions import Directions


@dataclass(frozen=True)
class AbcTile:
    name: str
    allowed_tiles: dict[Directions, set[str]]

    def __str__(self):
        return self.name

    def __rich__(self):
        return self.name

    def __post_init__(self):
        for direction in Directions:
            assert direction in self.allowed_tiles, f'Missing {direction} rule for {self.name} tile'
