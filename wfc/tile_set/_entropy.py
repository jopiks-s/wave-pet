from queue import Queue


def propagate_collapse(self, row, column):
    from wfc import TileSet, CellFrame, Tile
    self: TileSet

    q = Queue()
    q.put(self.board[row][column])

    while not q.empty():
        curr_cell: CellFrame = q.get()
        if curr_cell.finish:
            continue

        cell_neighbors = curr_cell.get_available_neighbors()

        for direction in Tile.Directions:
            next_row, next_col = self.get_coords(curr_cell.row, curr_cell.column, direction)
            if next_row is None or next_col is None:
                continue

            adjacent_cell: CellFrame = self.board[next_row][next_col]
            if adjacent_cell.apply_new_rules(cell_neighbors[direction]):
                q.put(adjacent_cell)
