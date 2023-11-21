from AbstractWFC.tile_set import TileSet
from .abc_cell import AbcCell, _StateController, _Actions
from ._state import State
from ._transformation_result import TransformationResult


class Cell(AbcCell, _StateController, _Actions):
    def __init__(self, tile_set: TileSet):
        pass
        # self.tile_set = tile_set
