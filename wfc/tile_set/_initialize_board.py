def _create_board(self, map_frm, board_frm):
    from . import TileSet
    from map import Map, BoardFrame
    from wfc import CellFrame

    self: TileSet
    map_frm: Map
    board_frm: BoardFrame

    board_dimension = map_frm.board_dimension
    scaled_imgs = self.resize_pack(int(map_frm.cell_size / self.cell_dim))
    for i in range(board_dimension):
        self.board.append([])
        for j in range(board_dimension):
            cell_frm = CellFrame(self, map_frm.cell_size, scaled_imgs, master=board_frm)
            cell_frm.grid(row=i, column=j, sticky='nsew')
            self.board[i].append(cell_frm)
