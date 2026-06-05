from collections import defaultdict
from random import choice
from typing import TypeVar, Generic

from .cell import Cell
from .tile_pack import AbcTilePack

CellT = TypeVar("CellT", bound=Cell)


class Board(Generic[CellT]):
    cell_cls: type[CellT] = Cell

    def __init__(self, size: int, tile_pack: AbcTilePack):
        self.tile_pack = tile_pack

        self._size = 0
        self._board: list[list[CellT]] = []
        self.change_size(size)

    @property
    def size(self) -> int:
        return self._size

    def change_size(self, new_size: int) -> None:
        assert new_size > 0, f'Size can`t be less then one. {new_size=}'
        if new_size == self._size:
            return

        self._size = new_size
        self._board = [[self.cell_cls(row, column, self.tile_pack, self._size) for column in range(self._size)] for row
                       in
                       range(self._size)]

    @staticmethod
    def is_on_board(row: int, column: int, board_size: int) -> bool:
        return 0 <= row < board_size and 0 <= column < board_size

    def choose_cell(self) -> CellT | None:
        entropy_groups = defaultdict(list)
        for row in self._board:
            for cell in row:
                if cell.entropy > 1:
                    entropy_groups[cell.entropy].append(cell)
        if len(entropy_groups) == 0:
            return None

        entropy_groups = dict(sorted(entropy_groups.items()))
        low_group = list(entropy_groups.values())[0]
        return choice(low_group)

    def _update_cell_neighbors(self, cell: CellT) -> set[CellT]:
        cell: Cell
        if cell.entropy == 0:
            return set()

        rules = cell.ruleset
        directions = cell.directions
        changed_cells = set()

        for direction in directions:
            _dir, coord = direction
            row, column = coord
            n_cell = self.get_cell(row, column)
            updated_tiles = n_cell.tiles.intersection(rules[_dir])

            if updated_tiles != n_cell.tiles:
                if len(updated_tiles) == 0:
                    print(f'Broke {n_cell=} by {cell}')
                n_cell.tiles = updated_tiles
                changed_cells.add(n_cell)

        return changed_cells

    def propagate_collapse(self, cell: CellT) -> set[CellT]:
        change_list = list(self._update_cell_neighbors(cell))
        all_changes = set(change_list)

        while change_list:
            changed_cell = change_list.pop()
            changes = self._update_cell_neighbors(changed_cell)
            all_changes.update(changes)
            change_list.extend(list(changes))

        return all_changes

    def is_broken(self) -> bool:
        for row in self._board:
            for cell in row:
                if cell.entropy == 0:
                    return True
        return False

    @property
    def solved_count(self) -> int:
        solved_count = 0
        for row in self._board:
            for cell in row:
                if cell.entropy <= 1:
                    solved_count += 1
        return solved_count

    @property
    def solved(self) -> bool:
        for row in self._board:
            for cell in row:
                if cell.entropy > 1:
                    return False
        return True

    def get_cell(self, row, column) -> CellT:
        if not Board.is_on_board(row, column, self._size):
            raise IndexError(f'{row=}, {column=}')
        return self._board[row][column]

    def solve(self):
        if self.solved:
            print('Board already solved')
            return

        while True:
            cell = self.choose_cell()
            if cell is None:
                break

            cell.collapse()
            self.propagate_collapse(cell)
        print('board solved')

    def reset(self):
        for row in self._board:
            for cell in row:
                cell.reset()
