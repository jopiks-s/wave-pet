from copy import copy
from queue import Queue

from tabulate import tabulate

from AbstractWFC.cell import Cell
from AbstractWFC.tile import Directions


class PropagationHistory:
    def __init__(self, board_size: int):
        self.board_size = board_size
        self._q = Queue()
        self._history = Queue()

    def get(self) -> tuple[Directions | None, Cell]:
        return self._q.get()

    def put(self, _dir: Directions | None, cell: Cell):
        self._q.put((_dir, cell))
        self._history.put((_dir, cell))

    def empty(self) -> bool:
        return self._q.empty()

    def get_history(self) -> Queue:
        return self._history

    def __str__(self):
        size = self.board_size
        _history = copy(self._history)
        headers = [''] + [i for i in range(0, size)]
        table = [[0 for j in range(size)] for i in range(size)]
        while not _history.empty():
            _dir, cell = _history.get()
            symbol = _dir.symbol() if _dir is not None else '.'
            table[cell.row][cell.column] = symbol

        return tabulate(table, headers, 'fancy_grid', showindex='always')

