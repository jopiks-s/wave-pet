import random
from abc import ABC

from AbstractWFC.cell import State
from AbstractWFC.cell.abc_cell import AbcCell


class Actions(AbcCell, ABC):
    def reset_cell(self):
        self.state = State.Stable
        self._tiles = self._tiles_clipboard.copy()

    def apply_rules(self, rules: list[str]) -> 'TransformationResult':
        assert self.state != State.Broken, f'Can`t apply rules when Cell state = {self.state}'

        items = []
        for tile_name in self._tiles:
            if tile_name not in rules:
                items.append(tile_name)

        return self.pop(items)

    def collapse_cell(self, tile_name: str | None = None) -> 'TransformationResult':
        assert self.state == State.Stable, f'Can`t collapse when Cell state = {self.state}'

        items = list(self._tiles)
        if tile_name is None:
            tile_name = random.choice(items)

        items.remove(tile_name)

        return self.pop(items)

from .._transformation_result import TransformationResult
