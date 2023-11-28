from abc import ABC

from AbstractWFC.board import AbcBoard, PropagationHistory
from AbstractWFC.cell import Cell, State
from AbstractWFC.tile import Directions


class Entropy(AbcBoard, ABC):
    def solve_board(self) -> list[PropagationHistory]:
        solve_history = []

        while not self.complete:
            min_entropy = float('inf')
            min_cell = None

            for i in range(self.size):
                for j in range(self.size):
                    cell = self._board[i][j]
                    entropy = cell.get_entropy()
                    if 1 < entropy < min_entropy:
                        min_entropy = entropy
                        min_cell = cell

            self.update_status(min_cell.collapse_cell())
            solve_history.append(self.propagate_collapse(min_cell))

        return solve_history

    def solve_cell(self, row: int, column: int) -> PropagationHistory | None:
        if not self.in_range(row, column):
            return
        cell = self._board[row][column]
        if cell.state != State.Stable:
            return

        self.update_status(cell.collapse_cell())
        return self.propagate_collapse(cell)

    def propagate_collapse(self, cell: Cell) -> PropagationHistory:
        q = PropagationHistory()

        q.put(None, cell)

        while not q.empty():
            curr_cell = q.get()
            if curr_cell.state == State.Broken:
                continue

            cell_neighbors = curr_cell.get_available_neighbors()
            for _dir in Directions:
                adjacent_cell = self.get(curr_cell, _dir)
                if adjacent_cell is None:
                    continue

                transfres = self.update_status(adjacent_cell.apply_rules(cell_neighbors[_dir]))
                if transfres.tiles_changed:
                    q.put(_dir, adjacent_cell)

        return q
