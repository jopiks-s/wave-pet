import tkinter as tk
from wfc import tile


# reduce entropy to zero by choosing tile for the cell
def collapse_cell(self, e: tk.Event):
    from . import CellFrame
    self: CellFrame

    self.select_image(e.widget)
    row, col = self.grid_info()['row'], self.grid_info()['column']
    self.tile_set.propagate_collapse(row, col)


def apply_new_rules(self, rules: list[str]):
    """Responds to new available tiles in a cell, removes unnecessary choices"""
    from . import CellFrame
    self: CellFrame

    to_delete = []
    for img_lbl, cell_tile in self.mapped_imgs.values():
        if cell_tile.name not in rules:
            to_delete.append(img_lbl)

    self.delete_images(to_delete)


def get_available_neighbors(self) -> tile.AvailableNeighbors:
    from . import CellFrame
    from wfc import tile, Tile
    self: CellFrame

    valid_adjacent = tile.AvailableNeighbors()

    for i, direction in enumerate(Tile.Directions):
        union_res = set()
        for cell_tile in self.mapped_imgs.values():
            union_res.update(cell_tile.rules[i])

        valid_adjacent[direction] = list(union_res)

    return valid_adjacent
