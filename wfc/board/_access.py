from wfc import CellFrame, Tile


def get(self, row: int, column: int, direction: Tile.Directions | None = None) -> CellFrame | None:
    row, column = self.get_coords(row, column, direction)
    if row is None or column is None:
        return

    return self._board[row][column]


def get_coords(self, row: int, column: int, direction: Tile.Directions | None = None) \
        -> tuple[int, int] | tuple[None, None]:
    match direction:
        case Tile.Directions.UP:
            row -= 1
        case Tile.Directions.RIGHT:
            column += 1
        case Tile.Directions.DOWN:
            row += 1
        case Tile.Directions.LEFT:
            column -= 1
        case None:
            ...

    if 0 <= row < self.dim and 0 <= column < self.dim:
        return row, column
    return None, None
