from wfc import TileSet


class Board:
    from ._manager import _create_board, reset_board
    from ._access import get, get_coords
    from ._entropy import propagate_collapse, auto_solve

    def __init__(self, dim: int, tile_set: TileSet, board_frm):
        from wfc import CellFrame
        from map import BoardFrame
        board_frm: BoardFrame

        self.dim = dim
        self.tile_set = tile_set
        self.board_frame = board_frm
        # todo: make it property for resolution track
        self.complete = -1
        self._board: list[list[CellFrame]] = []

        self._create_board()
