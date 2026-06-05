from pathlib import Path

from rich.console import Console
from rich.text import Text

from .board import Board
from .tile_pack import TextTilePack

SIZE = 25
ITERATIONS = 15
PACKS = ['road', 'forrest-sea', 'network']
TILES_PATH = Path(__file__).parent.parent / 'tile_packs' / 'text' / PACKS[0]

tile_pack = TextTilePack(TILES_PATH)
board = Board(SIZE, tile_pack)
console = Console()

for i in range(ITERATIONS):
    board.solve()
    board.reset()
    console.print(Text(f'done {i}', 'dim'))
exit(0)
