def _create_board(self, cell_size: int):
    from wfc import Board, CellFrame
    self: Board

    img_size = int(cell_size / self.tile_set.square_bound)
    scaled_imgs = self.tile_set.get_resized(img_size)
    for i in range(self.dim):
        self._board.append([])
        for j in range(self.dim):
            cell_frm = CellFrame(self.board_frame, self, self.tile_set, scaled_imgs, cell_size)
            padx = (self.board_frame.to_padx, 0) if j == 0 else (0, 0)
            pady = (self.board_frame.to_pady, 0) if i == 0 else (0, 0)

            cell_frm.grid(row=i, column=j, sticky='nsew', padx=padx, pady=pady)

            self._board[i].append(cell_frm)

    self.size = self.dim * self.dim
    self.complete.set(False)
    self.solved.set(0)
    self.real_size.set(self.size)


def reset_board(self):
    from . import Board
    self: Board

    self.complete.set(False)
    self.solved.set(0)
    self.real_size.set(self.size)
    for cell_frm in sum(self._board, []):
        cell_frm.reset_cell()
