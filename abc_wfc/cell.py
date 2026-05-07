from random import choice

from .directions import Directions
from .tile_pack import AbcTilePack


class Cell:
    def __init__(self, row: int, column: int, tile_pack: AbcTilePack, board_size: int):
        self.row = row
        self.column = column
        self.tile_pack = tile_pack
        self._tiles = tile_pack.keys()
        self.board_size = board_size
        self.directions = self._create_directions()

    def __repr__(self):
        return f'cell{{{self.row}, {self.column}, {self.entropy}}}'

    def _create_directions(self) -> tuple[tuple[Directions, tuple[int, int]], ...]:
        from .board import Board

        possible_directions = (
            (Directions.UP, (self.row - 1, self.column)),
            (Directions.RIGHT, (self.row, self.column + 1)),
            (Directions.DOWN, (self.row + 1, self.column)),
            (Directions.LEFT, (self.row, self.column - 1)))

        return tuple((direction, coord) for direction, coord in possible_directions
                     if Board.is_on_board(*coord, self.board_size))

    @property
    def tiles(self) -> set[str]:
        return self._tiles

    @tiles.setter
    def tiles(self, value: set[str]):
        self._tiles = value

    @property
    def ruleset(self) -> dict[Directions, set[str]]:
        rules = {d: set() for d in Directions}
        for tile_name in self._tiles:
            for direction in Directions:
                allowed_tiles = self.tile_pack[tile_name].allowed_tiles[direction]
                rules[direction].update(allowed_tiles)

        return rules

    @property
    def entropy(self) -> int:
        return len(self._tiles)

    def reset(self):
        self._tiles = self.tile_pack.keys()

    def collapse(self) -> str:
        self._tiles = {choice(list(self._tiles)), }
        return self.collapsed_tile

    @property
    def collapsed_tile(self) -> str:
        if self.entropy > 1:
            raise ValueError('Cell is not collapsed')
        else:
            return next(iter(self._tiles))
