from dataclasses import dataclass, field

from ._directions import Directions


@dataclass(frozen=True)
class Tile:
    name: str
    rules: dict[Directions, list[str]] = field()

    def __post_init__(self):
        for direction in Directions:
            assert direction in self.rules, f'Missing rule for {direction=} in __init__'
