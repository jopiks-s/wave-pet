sequence = '''6, 2; blank
5, 2; blank
4, 2; left
6, 1; blank
6, 3; blank
5, 0; blank
5, 4; down
4, 4; right
3, 4; blank
3, 5; blank
2, 5; left
2, 3; down
2, 2; up
2, 1; right
3, 6; down
3, 0; right
1, 1; blank
0, 1; blank
2, 6; right
5, 5; left
4, 6; left
1, 6; left
1, 5; right
0, 5; blank
0, 4; blank'''
# map_size = 7

s = sequence1.split('\n')
for r in s:
    row, column, tile = r.split(',')
    row = int(row.strip('row='))
    column = int(column.strip(' column='))
    tile = tile.strip()
    print(f'print(f\'collapse {row}, {column}, {tile}\')')
    print(f'board._board[{row}][{column}].tiles = {{\'{tile}\',}}')
    print(f'board.propagate_collapse(board._board[{row}][{column}])')
    print(f'board.draw_board()')

print('\n\n')

for r in s:
    row, column, tile = r.split(',')
    row = int(row.strip('row='))
    column = int(column.strip(' column='))
    tile = tile.strip()
    print(f'print(f\'collapse {row}, {column}, {tile}\')')
    print(f'board[{row}][{column}] = {{\'{tile}\',}}')
    print(f'update_neighbors({column}, {row})')
    print(f'draw_board()')
