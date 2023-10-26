from wfc import TileSet, CellFrame


class Board:
    from ._access import get, get_coords

    def __init__(self, dim: int, tile_set: TileSet, board_frm):
        from map import BoardFrame
        board_frm: BoardFrame

        self.dim = dim
        self.tile_set = tile_set
        self.board_frame = board_frm
        self.complete = -1
        self._board = []

        self._create_board()

    def _create_board(self):
        scaled_imgs = self.tile_set.resize_pack(int(self.board_frame.cell_size / self.tile_set.cell_dim))
        for i in range(self.dim):
            self._board.append([])
            for j in range(self.dim):
                cell_frm = CellFrame(self.tile_set, self.board_frame.cell_size, scaled_imgs, master=self.board_frame)
                cell_frm.grid(row=i, column=j, sticky='nsew')
                self._board[i].append(cell_frm)

    def reset_board(self):
        ...
