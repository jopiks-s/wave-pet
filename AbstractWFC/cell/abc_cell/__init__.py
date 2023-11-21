import abc
from abc import ABC

from AbstractWFC.cell import State, TransformationResult
from AbstractWFC.tile import Tile
from AbstractWFC.tile_set import TileSet


class AbcCell(ABC):
    _tiles: dict[str, Tile] = None
    _tiles_clipboard: dict[str, Tile] = None
    _state: State = None
    _tile_set: TileSet = None
    _row: int = None
    _column: int = None

    @abc.abstractmethod
    def __init__(self, tile_set: TileSet):
        pass
    @property
    @abc.abstractmethod
    def tiles(self):
        pass

    @property
    @abc.abstractmethod
    def tiles_clipboard(self):
        pass

    @property
    @abc.abstractmethod
    def state(self):
        pass

    @property
    @abc.abstractmethod
    def tile_set(self):
        pass

    @property
    @abc.abstractmethod
    def row(self):
        pass

    @property
    @abc.abstractmethod
    def column(self):
        pass

    @abc.abstractmethod
    def reset_cell(self) -> None:
        pass

    @abc.abstractmethod
    def apply_rules(self, rules: list[str]) -> TransformationResult:
        pass

    @abc.abstractmethod
    def collapse_cell(self, tile_name: str | None = None) -> TransformationResult:
        pass

    @abc.abstractmethod
    def pop(self, items: list[Tile] | Tile) -> TransformationResult:
        pass


from ._state_controller import _StateController
from ._actions import _Actions
