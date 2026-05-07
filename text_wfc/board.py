from abc_wfc import Board as BaseBoard


class Board(BaseBoard):
    def solve(self):
        super().solve()
        self.draw_board()

    def draw_board(self):
        for row in self._board:
            for cell in row:
                entropy = cell.entropy
                symbol = f'{entropy}'
                if entropy == 1:
                    symbol = self.tile_pack[cell.collapsed_tile].represent()
                print(symbol, end=' ')
            print()
