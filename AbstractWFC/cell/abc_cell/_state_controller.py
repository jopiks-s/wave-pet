from abc import ABC

from AbstractWFC.cell import State
from AbstractWFC.cell.abc_cell import AbcCell


class StateController(AbcCell, ABC):
    def pop(self, items: list[str] | str) -> 'TransformationResult':
        if not isinstance(items, list):
            items = [items]

        transform_res = TransformationResult(self, True, self.state, self.state)
        tiles_left = len(self._tiles) - len(items)
        if tiles_left == 0:
            self.state = State.Broken
            transform_res.curr_state = self.state
        elif tiles_left == 1:
            self.state = State.Collapsed
            transform_res.curr_state = self.state

        for tile_name in items:
            assert tile_name in self._tiles, f'The tile does not belong in this cell, {tile_name=}'
            self._tiles.pop(tile_name)

        return transform_res


from .._transformation_result import TransformationResult
