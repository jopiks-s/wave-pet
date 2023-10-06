import tkinter as tk


# reduce entropy to zero by choosing tile for the cell
def collapse_cell(self, e: tk.Event):
    ...


# update the available tiles in the cell from which to choose
# according to new rules
def update_cell(self, new_rules):
    ...
