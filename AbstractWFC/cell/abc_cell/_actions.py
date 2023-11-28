import random
from abc import ABC

from AbstractWFC.cell import State
from AbstractWFC.cell.abc_cell import AbcCell
from AbstractWFC.tile import Directions


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

    def get_available_neighbors(self) -> dict[Directions, list[str]] | None:
        if self.state == State.Broken:
            return

        available_neighbors = {_dir: set() for _dir in Directions}
        for tile in self._tiles.values():
            for _dir in Directions:
                available_neighbors[_dir].update(tile.rules[_dir])

        return {_dir: list(neighbors) for _dir, neighbors in available_neighbors.items()}

    def get_entropy(self) -> int:
        """Return -1 if Broken, 0 if Collapsed, positive int if Stable"""
        if self.state == State.Broken:
            return -1
        if self.state == State.Collapsed:
            return 0
        if self.state == State.Stable:
            return len(self._tiles)


from .._transformation_result import TransformationResult