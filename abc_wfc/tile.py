from abc import ABC, abstractmethod
from dataclasses import dataclass

from .directions import Directions


@dataclass(frozen=True)
class AbcTile(ABC):
    name: str
    allowed_tiles: dict[Directions, set[str]]

    @abstractmethod
    def represent(self):
        pass

    def __post_init__(self):
        for direction in Directions:
            assert direction in self.allowed_tiles, f'Missing {direction} rule for {self.name} tile'
