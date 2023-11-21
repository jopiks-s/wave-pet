from abc import ABC

from AbstractWFC.cell import TransformationResult, State
from AbstractWFC.cell.abc_cell import AbcCell
from AbstractWFC.tile import Tile


class _StateController(AbcCell, ABC):
    def pop(self, items: list[Tile] | Tile) -> TransformationResult:
        tiles_left = len(self.tiles) - len(items)
        transform_res = TransformationResult(self, False, self.state, self.state)
        if tiles_left == 0:
            self.state = State.Broken
            self.tiles_clipboard
            self.tiles =

        return transform_res
