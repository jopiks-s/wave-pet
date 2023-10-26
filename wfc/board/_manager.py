def _create_board(self):
    from wfc import Board, CellFrame
    self: Board

    img_size = int(self.board_frame.cell_size / self.tile_set.get_square_bound())
    scaled_imgs = self.tile_set.resize_pack(img_size)
    for i in range(self.dim):
        self._board.append([])
        for j in range(self.dim):
            cell_frm = CellFrame(self, self.tile_set, self.board_frame.cell_size, scaled_imgs,
                                 master=self.board_frame)
            cell_frm.grid(row=i, column=j, sticky='nsew')
            self._board[i].append(cell_frm)

    self.complete = 0


def reset_board(self):
    from wfc import Board
    self: Board

    self.complete = 0
    for cell_frm in sum(self._board, []):
        cell_frm.reset_cell()
