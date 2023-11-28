from abc import ABC

from AbstractWFC.board import AbcBoard
from AbstractWFC.cell import Cell
from AbstractWFC.tile import Directions


class Get(AbcBoard, ABC):
    def get(self, cell: Cell, _dir: Directions) -> Cell | None:
        row, column = cell.row, cell.column

        match _dir:
            case Directions.UP:
                row -= 1
            case Directions.RIGHT:
                column += 1
            case Directions.DOWN:
                row += 1
            case Directions.LEFT:
                column -= 1

        if not self.in_range(row, column):
            return None

        return self._board[row][column]

    def in_range(self, row: int, column: int) -> bool:
        return 0 <= row < self.size and 0 <= column < self.size
