from queue import Queue


def propagate_collapse(self, cell_frm):
    from wfc import Board, CellFrame, Tile
    self: Board
    cell_frm: CellFrame

    q = Queue()
    q.put(cell_frm)

    while not q.empty():
        curr_cell: CellFrame = q.get()
        if curr_cell.state == CellFrame.State.Broken:
            continue

        cell_neighbors = curr_cell.get_available_neighbors()

        for direction in Tile.Directions:
            adjacent_cell = self.get(curr_cell.row, curr_cell.column, direction)
            if adjacent_cell is None:
                continue

            if adjacent_cell.apply_new_rules(cell_neighbors[direction]):
                q.put(adjacent_cell)


def auto_solve(self):
    from wfc import Board, CellFrame
    self: Board

    if self.complete.get():
        return

    max_entropy = float('inf')
    min_entropy = [float('inf'), None]

    while max_entropy > 1:
        max_entropy = -1
        min_entropy[0] = float('inf')
        # find min entropy cell
        for i in range(self.dim):
            for j in range(self.dim):
                cell_frm: CellFrame = self.get(i, j)
                cell_entropy = cell_frm.get_entropy()
                max_entropy = max(max_entropy, cell_entropy)
                if cell_entropy > 1:
                    if min_entropy[0] > cell_entropy:
                        min_entropy[0] = cell_entropy
                        min_entropy[1] = cell_frm

        if min_entropy[0] == float('inf'):
            continue

        min_entropy[1].collapse_cell()
        self.propagate_collapse(min_entropy[1])

    assert self.complete.get(), 'Must be complete'
