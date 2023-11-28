from AbstractWFC.cell import Cell
from AbstractWFC.tile_set import TileSet

from .propagation_history import PropagationHistory

from ._abc_board import AbcBoard
from ._entropy import Entropy
from ._get import Get
from ._status_handler import StatusHandler


class Board(Entropy, StatusHandler, Get):
    def __init__(self, tile_set: TileSet, size: int):
        self.size = size
        self.cell_number = size ** 2

        self.reset_status()
        self._board = [[Cell(i, j, tile_set) for j in range(size)] for i in range(size)]
