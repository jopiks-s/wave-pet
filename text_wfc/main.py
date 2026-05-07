from board import Board
from tile_pack import TextTilePack

map_size = 15
iterations = 100

road_pack = TextTilePack('tiles/road')
board = Board(map_size, road_pack)

for i in range(iterations):
    board.solve()
    board.reset()
    print(f'done {i}')
exit(0)
