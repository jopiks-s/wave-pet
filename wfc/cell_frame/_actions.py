import tkinter as tk


# reduce entropy to zero by choosing tile for the cell
def collapse_cell(self, e: tk.Event):
    from . import CellFrame
    self: CellFrame

    self.select_image(e.widget)
    row, col = self.grid_info()['row'], self.grid_info()['column']
    self.tile_set.propagate_collapse(row, col)


# update the available tiles in the cell from which to choose
# according to new rules
def reduce_entropy(self, new_rules):
    ...
