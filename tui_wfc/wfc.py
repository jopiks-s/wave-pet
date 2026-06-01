from rich.text import Text

from abc_wfc import Board as BaseBoard
from abc_wfc.cell import Cell as BaseCell
from text_wfc.tile_pack import TextTilePack


class Cell(BaseCell):
    tile_pack: TextTilePack

    def __rich__(self) -> Text:
        match self.entropy:
            case 0:
                return Text('X', 'dim')
            case 1:
                return self.tile_pack[self.collapsed_tile].symbol
            case entropy:
                return Text(str(entropy))


class Board(BaseBoard[Cell]):
    cell_cls = Cell
