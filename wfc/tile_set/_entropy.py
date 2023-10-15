from queue import Queue


def propagate_collapse(self, cell_frm):
    from wfc import TileSet, Tile, CellFrame
    self: TileSet
    cell_frm: CellFrame

    q = Queue()
    q.put(self.board[cell_frm.row][cell_frm.column])

    while not q.empty():
        curr_cell: CellFrame = q.get()
        if curr_cell.state == CellFrame.State.Broken:
            continue

        cell_neighbors = curr_cell.get_available_neighbors()

        for direction in Tile.Directions:
            next_row, next_col = self.get_coords(curr_cell.row, curr_cell.column, direction)
            if next_row is None or next_col is None:
                continue

            adjacent_cell: CellFrame = self.board[next_row][next_col]
            if adjacent_cell.apply_new_rules(cell_neighbors[direction]):
                q.put(adjacent_cell)


def auto_solve(self):
    from wfc import TileSet, CellFrame
    self: TileSet

    max_entropy = -1
    min_entropy = [float('inf'), None]
    board_dimension = self.map_frm.board_dimension

    while max_entropy != 0:
        max_entropy = -1
        min_entropy[0] = float('inf')
        for i in range(board_dimension):
            for j in range(board_dimension):
                cell_frm: CellFrame = self.board[i][j]
                cell_entropy = cell_frm.get_entropy()
                if isinstance(cell_entropy, CellFrame.State):
                    max_entropy = max(max_entropy, 0)
                    continue

                max_entropy = max(max_entropy, cell_entropy)
                if min_entropy[0] > cell_entropy:
                    min_entropy[0] = cell_entropy
                    min_entropy[1] = cell_frm

        if min_entropy[1] is None:
            continue

        min_entropy[1].collapse_cell()
        self.propagate_collapse(min_entropy[1])
