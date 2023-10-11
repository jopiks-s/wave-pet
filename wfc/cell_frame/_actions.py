import tkinter as tk
from wfc import tile


def collapse_cell(self, e: tk.Event):
    from . import CellFrame
    self: CellFrame

    # [TODO] add a handler when only one tile remains
    if len(self.mapped_imgs) == 1:
        return

    self.select_image(e.widget)
    self.tile_set.propagate_collapse(self.row, self.column)


def apply_new_rules(self, rules: list[str]) -> bool:
    """Responds to new available tiles in a cell, removes unnecessary choices.
    Returns True if the cell tiles have been changed, False otherwise"""
    from . import CellFrame
    self: CellFrame

    to_delete = []
    for img_lbl, cell_tile in self.mapped_imgs.items():
        if cell_tile.name not in rules:
            to_delete.append(img_lbl)

    self.delete_images(to_delete)
    return len(to_delete) > 0


def get_available_neighbors(self) -> tile.AvailableNeighbors | None:
    from . import CellFrame
    from wfc import tile, Tile
    self: CellFrame

    if not len(self.mapped_imgs):
        return

    valid_adjacent = tile.AvailableNeighbors()

    for i, direction in enumerate(Tile.Directions):
        union_res = set()
        for cell_tile in self.mapped_imgs.values():
            union_res.update(cell_tile.rules[i])

        valid_adjacent[direction] = list(union_res)

    return valid_adjacent
