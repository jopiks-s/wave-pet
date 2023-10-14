from random import choice
from typing import TypeVar

from wfc import tile


def collapse_cell(self, img_lbl=None):
    """Reduce entropy to 0 by choosing one of the remaining tiles in the cell.
    If argument 'img_lbl' wasn`t passed, random tile is selected"""
    from . import CellFrame
    from image_label import ImageLabel
    self: CellFrame
    img_lbl: ImageLabel | None

    if self.state != CellFrame.State.Stable:
        return
    assert len(self.mapped_imgs) > 1

    self.State = CellFrame.State.Collapsed
    if img_lbl is None:
        img_lbl = choice(self.mapped_imgs)

    self.select_image(img_lbl)


def apply_new_rules(self, rules: list[str]) -> bool:
    """Responds to new available tiles in a cell, removes unnecessary choices.
    Returns True if the cell tiles have been changed, False otherwise"""
    from . import CellFrame
    self: CellFrame

    to_delete = []
    for img_lbl, cell_tile in self.mapped_imgs.items():
        if cell_tile.name not in rules:
            to_delete.append(img_lbl)

    if len(to_delete) == len(self.mapped_imgs):
        self.state = CellFrame.State.Broken

    self.delete_images(to_delete)
    return len(to_delete) > 0


def get_available_neighbors(self) -> tile.AvailableNeighbors | None:
    from . import CellFrame
    from wfc import tile, Tile
    self: CellFrame

    assert len(self.mapped_imgs), 'Access cell without tiles!'

    valid_adjacent = tile.AvailableNeighbors()

    for i, direction in enumerate(Tile.Directions):
        union_res = set()
        for cell_tile in self.mapped_imgs.values():
            union_res.update(cell_tile.rules[i])

        valid_adjacent[direction] = list(union_res)

    return valid_adjacent


IntOrState = TypeVar('IntOrState')


def get_entropy(self) -> IntOrState:
    """Return int if neither collapsed nor broken, otherwise State of the cell"""
    from . import CellFrame
    self: CellFrame

    if self.state != CellFrame.State.Stable:
        return self.state

    return len(self.mapped_imgs)
