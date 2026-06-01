from rich.text import Text
from typing import Literal

from abc_wfc import Board as BaseBoard
from abc_wfc.cell import Cell as BaseCell
from text_wfc.tile_pack import TextTilePack


class Cell(BaseCell):
    tile_pack: TextTilePack
    highlighted: bool = False
    _highlighted_tile: Text = Text('  ', 'on yellow')
    level_styles = {'low': 'bright_yellow', 'medium': 'yellow', 'high': 'dim'}

    def entropy_level(self) -> Literal['low', 'medium', 'high']:
        level = self.entropy/self.tile_pack.size
        if level < .4:
            return 'low'
        elif level < .7:
            return 'medium'
        else:
            return 'high'

    def __rich__(self) -> Text:
        match self.entropy:
            case 0:
                return Text('X', 'dim')
            case 1:
                if self.highlighted:
                    return self._highlighted_tile
                else:
                    return self.tile_pack[self.collapsed_tile].symbol
            case entropy:
                if self.highlighted:
                    return self._highlighted_tile
                else:
                    level = self.entropy_level()
                    if level == 'high':
                        entropy = '·'
                    return Text(str(entropy), self.level_styles[level])


class Board(BaseBoard[Cell]):
    cell_cls = Cell
