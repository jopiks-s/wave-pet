import abc
from abc import ABC

from AbstractWFC.board import PropagationHistory
from AbstractWFC.cell import Cell, TransformationResult
from AbstractWFC.tile import Directions


class AbcBoard(ABC):
    _board: list[list[Cell]] = None

    @abc.abstractmethod
    def get(self, cell: Cell, _dir: Directions) -> Cell | None:
        pass

    @abc.abstractmethod
    def in_range(self, row: int, column: int) -> bool:
        pass

    size: int = None
    cell_number: int = None
    stable_counter: int = None
    collapsed_counter: int = None
    complete: bool = None

    @abc.abstractmethod
    def __init__(self, size: int):
        pass

    @abc.abstractmethod
    def solve_board(self):
        pass

    @abc.abstractmethod
    def solve_cell(self, row: int, column: int):
        pass

    @abc.abstractmethod
    def propagate_collapse(self, cell: Cell) -> PropagationHistory:
        pass

    @abc.abstractmethod
    def reset_board(self):
        pass

    @abc.abstractmethod
    def update_status(self, transfres: TransformationResult) -> TransformationResult:
        pass

    @abc.abstractmethod
    def reset_status(self):
        pass
