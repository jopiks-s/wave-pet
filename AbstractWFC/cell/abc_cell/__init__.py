import abc
from abc import ABC

from AbstractWFC.cell import State
from AbstractWFC.tile import Tile, Directions
from AbstractWFC.tile_set import TileSet


class AbcCell(ABC):
    _tiles: dict[str, Tile] = None
    _tiles_clipboard: dict[str, Tile] = None

    @abc.abstractmethod
    def get_available_neighbors(self) -> dict[Directions, list[str]] | None:
        pass

    @abc.abstractmethod
    def get_entropy(self) -> int:
        pass

    @abc.abstractmethod
    def pop(self, items: list[str] | str) -> 'TransformationResult':
        pass

    state: State = None
    tile_set: TileSet = None
    row: int = None
    column: int = None

    @abc.abstractmethod
    def __init__(self, row: int, column: int, tile_set: TileSet):
        pass

    @abc.abstractmethod
    def reset_cell(self) -> None:
        pass

    @abc.abstractmethod
    def apply_rules(self, rules: list[str]) -> 'TransformationResult':
        pass

    @abc.abstractmethod
    def collapse_cell(self, tile_name: str | None = None) -> 'TransformationResult':
        pass


from .._transformation_result import TransformationResult
from ._state_controller import StateController
from ._actions import Actions
