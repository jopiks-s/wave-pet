from queue import Queue

from AbstractWFC.cell import Cell
from AbstractWFC.tile import Directions


class PropagationHistory:
    def __init__(self):
        self._q = Queue()
        self._history = Queue()

    def get(self) -> Cell:
        return self._q.get()

    def put(self, _dir: Directions | None, cell: Cell):
        self._q.put(cell)
        self._history.put((_dir, cell))

    def empty(self) -> bool:
        return self._q.empty()

    def get_history(self) -> Queue:
        return self._history
