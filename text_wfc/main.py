from pathlib import Path

from .board import Board
from .tile_pack import TextTilePack

map_size = 20
iterations = 10

TILES_PATH = Path(__file__).parent.parent / 'tiles' / 'text' / 'forrest-sea'
tile_pack = TextTilePack(TILES_PATH)
board = Board(map_size, tile_pack)

for i in range(iterations):
    board.solve()
    board.reset()
    print(f'done {i}')
exit(0)
