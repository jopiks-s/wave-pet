def _create_board(self):
    from wfc import Board, CellFrame
    self: Board

    img_size = int(self.board_frame.cell_size / self.tile_set.get_square_bound())
    scaled_imgs = self.tile_set.resize_pack(img_size)
    cell_size = self.board_frame.cell_size
    for i in range(self.dim):
        self._board.append([])
        for j in range(self.dim):
            cell_frm = CellFrame(self, self.tile_set, cell_size, scaled_imgs,
                                 width=cell_size, height=cell_size,
                                 master=self.board_frame)
            if j == 0:
                cell_frm.grid(row=i, column=j, sticky='nsew', padx=(self.board_frame.to_padx, 0))
            if i == 0:
                cell_frm.grid(row=i, column=j, sticky='nsew', pady=(self.board_frame.to_pady, 0))

            cell_frm.grid(row=i, column=j, sticky='nsew')

            self._board[i].append(cell_frm)

    self.size = self.dim * self.dim
    self.solved.set(0)
    self.real_size.set(self.size)


def reset_board(self):
    from wfc import Board
    self: Board

    self.complete = False
    self.solved.set(0)
    self.real_size.set(self.size)
    for cell_frm in sum(self._board, []):
        cell_frm.reset_cell()
