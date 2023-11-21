from AbstractWFC.tile_set import TileSet
from ._state import State
from ._transformation_result import TransformationResult
from .abc_cell import AbcCell, StateController, Actions


class Cell(StateController, Actions):
    def __init__(self, row: int, column: int, tile_set: TileSet):
        self.row = row
        self.column = column
        self.tile_set = tile_set

        self._tiles = tile_set.copy()
        self._tiles_clipboard = tile_set.copy()
        self.state = State.Stable
