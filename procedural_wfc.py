import json
from collections import defaultdict
from random import choice


def get_ruleset(x, y):
    rules = {d: set() for d in DIRECTIONS}
    for tile in board[y][x]:
        for direction in DIRECTIONS:
            rules[direction].update(pack[tile][direction])

    return rules


def get_neighbors(x, y):
    neighbors = [((x, y - 1), 'UP'), ((x + 1, y), 'RIGHT'), ((x, y + 1), 'DOWN'), ((x - 1, y), 'LEFT')]
    for neighbor, direction in neighbors[:]:
        for coord in neighbor:
            if coord < 0 or coord >= map_size:
                neighbors.remove((neighbor, direction))
                break

    return tuple(neighbors)


def tile_symbol(tile):
    match tile:
        case 'blank':
            return '□'
        case 'up':
            return '↑'
        case 'right':
            return '→'
        case 'down':
            return '↓'
        case 'left':
            return '←'
        case _:
            return tile


def draw_board():
    for row in board:
        for cell in row:
            cell_n = len(cell)
            symbol = tile_symbol(next(iter(cell))) if cell_n == 1 else cell_n
            print(symbol, end=' ')
        print()


def choose_cell() -> tuple[int, int] | None:
    entropy_groups = defaultdict(list)
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            entropy = len(cell)
            if entropy > 1:
                entropy_groups[entropy].append((x, y))
    if not len(entropy_groups):
        return None

    entropy_groups = dict(sorted(entropy_groups.items()))
    return choice(list(entropy_groups.values())[0])


def reset_board():
    board.clear()
    for i in range(map_size):
        board.append([])
        for _ in range(map_size):
            board[i].append(all_tiles.copy())


def update_neighbors(x, y):
    if len(board[y][x]) == 0:
        return

    rules = get_ruleset(x, y)
    neighbors = get_neighbors(x, y)
    changed_neighbors = set()
    for neighbor, directoin in neighbors:
        allowed_tiles = rules[directoin]
        n_tiles = board[neighbor[1]][neighbor[0]]
        updated_tiles = n_tiles.intersection(allowed_tiles)

        if updated_tiles != n_tiles:
            board[neighbor[1]][neighbor[0]] = updated_tiles
            if len(updated_tiles) == 0:
                print(f'Broke cell {neighbor}')
            changed_neighbors.add(neighbor)

    for changed_neighbor in changed_neighbors:
        update_neighbors(*changed_neighbor)


def has_broken() -> bool:
    for row in board:
        for cell in row:
            if len(cell) == 0:
                return True
    return False


DIRECTIONS = ['UP', 'RIGHT', 'DOWN', 'LEFT']
map_size = 5
board: list[list[set]] = []
with open('tk_wfc/tiles/road/ruleset.json', 'r') as f:
    pack = json.load(f)
all_tiles = set(pack.keys())

broken_counter = 0
iterations = 500
reset_board()

for i in range(iterations):
    while True:
        cell = choose_cell()
        if cell is None:
            draw_board()
            if has_broken():
                broken_counter += 1
                print('has broken')
            reset_board()
            break
        x, y = cell
        collapsed_tile = choice(list(board[y][x]))
        # print(f'collapse {x}, {y}; {collapsed_tile}')
        board[y][x] = {collapsed_tile}
        update_neighbors(x, y)

    print(f'DONE {i}\n')

print(f'{broken_counter}/{iterations}')

# print(f'collapse 2, 0, left')
# board[2][0] = {'left',}
# update_neighbors(0, 2)
# draw_board()
# print(f'collapse 2, 1, blank')
# board[2][1] = {'blank',}
# update_neighbors(1, 2)
# draw_board()
# print(f'collapse 2, 2, right')
# board[2][2] = {'right',}
# update_neighbors(2, 2)
# draw_board()
# print(f'collapse 1, 1, up')
# board[1][1] = {'up',}
# update_neighbors(1, 1)
# draw_board()
# print(f'collapse 1, 0, down')
# board[1][0] = {'down',}
# update_neighbors(0, 1)
# draw_board()
# print(f'collapse 1, 2, down')
# board[1][2] = {'down',}
# update_neighbors(2, 1)
# draw_board()
# print(f'collapse 0, 0, blank')
# board[0][0] = {'blank',}
# update_neighbors(0, 0)
# draw_board()
# print(f'collapse 0, 2, blank')
# board[0][2] = {'blank',}
# update_neighbors(2, 0)
