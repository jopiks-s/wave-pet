from random import choice

from wfc import tile


def reset_cell(self):
    from . import CellFrame
    self: CellFrame

    if self.state == CellFrame.State.Broken:
        self._undo_fill_empty_cell()

    self.max_side = self.tile_set.get_square_bound()
    self.state = CellFrame.State.Stable
    self._delete_all_images()
    self.create_from_tile_set()


def collapse_cell(self, img_lbl=None):
    """Reduce entropy to 0 by choosing one of the remaining tiles in the cell.
    If argument 'img_lbl' wasn`t passed, random tile is selected"""
    from . import CellFrame
    from image_label import ImageLabel
    self: CellFrame
    img_lbl: ImageLabel | None

    if self.state != CellFrame.State.Stable:
        return
    assert len(self.mapped_imgs) > 1, f'tiles left: {len(self.mapped_imgs)}'

    if img_lbl is None:
        img_lbl = choice(list(self.mapped_imgs))
    self._select_image(img_lbl)

    self.state = CellFrame.State.Collapsed
    # todo: fix 100/98(-2), how does it happen???
    self.board.complete.set(self.board.complete.get() + 1)


def apply_new_rules(self, rules: list[str]) -> bool:
    """Responds to new available tiles in a cell, removes unnecessary choices.
    Returns True if the cell tiles have been changed, False otherwise"""
    from . import CellFrame
    self: CellFrame

    to_delete = []
    mapped_copy = self.mapped_imgs.copy()
    for img_lbl, cell_tile in self.mapped_imgs.items():
        if cell_tile.name not in rules:
            del mapped_copy[img_lbl]
            to_delete.append(img_lbl)
    changed = len(to_delete) > 0

    if changed:
        if len(mapped_copy) == 0:
            self._delete_images(to_delete)
            self.state = CellFrame.State.Broken
            self.board.real_size.set(self.board.real_size.get() - 1)

        elif len(mapped_copy) == 1:
            self.collapse_cell(next(iter(mapped_copy)))
        else:
            self._delete_images(to_delete)

    return changed


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


def get_entropy(self) -> int:
    """Return -1 if Broken, 0 if Collapsed, positive int if Stable"""
    from . import CellFrame
    self: CellFrame

    match self.state:
        case CellFrame.State.Broken:
            return -1
        case CellFrame.State.Collapsed:
            return 0
        case CellFrame.State.Stable:
            return len(self.mapped_imgs)
