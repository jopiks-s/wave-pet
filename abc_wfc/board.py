from collections import defaultdict
from random import choice

from .cell import Cell
from .tile_pack import AbcTilePack


class Board:
    def __init__(self, size: int, tile_pack: AbcTilePack):
        self.size = size
        self.tile_pack = tile_pack
        self._board = [[Cell(row, column, tile_pack, size) for column in range(size)] for row in
                       range(size)]
        self.solved = False

    @staticmethod
    def is_on_board(row: int, column: int, board_size: int) -> bool:
        return 0 <= row < board_size and 0 <= column < board_size

    def reset(self):
        for row in self._board:
            for cell in row:
                cell.reset()
        self.solved = False

    def get_cell(self, row, column) -> Cell:
        if not Board.is_on_board(row, column, self.size):
            raise IndexError(f'{row=}, {column=}')
        return self._board[row][column]

    def choose_cell(self) -> 'Cell | None':
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

    def propagate_collapse(self, cell: 'Cell'):
        if cell.entropy == 0:
            return

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

        for changed_cell in changed_cells:
            self.propagate_collapse(changed_cell)

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
        self.solved = True

    def is_broken(self) -> bool:
        for row in self._board:
            for cell in row:
                if cell.entropy == 0:
                    return True
        return False
