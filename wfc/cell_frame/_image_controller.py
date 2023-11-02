import tkinter as tk
from math import ceil, sqrt

import customtkinter as ctk

from . import ImageLabel


def image_click_handler(self, e: tk.Event):
    from . import CellFrame
    self: CellFrame

    img_lbl = e.widget.master
    assert isinstance(img_lbl, ImageLabel), f'Incorrect type passed for this handler: {type(e.widget)}'
    # todo: add a handler when clicked and cell is already collapsed

    if len(self.mapped_imgs) == 1:
        assert self.state == CellFrame.State.Collapsed
        return

    self.collapse_cell(img_lbl)
    self.board.propagate_collapse(self)


def _select_image(self, img_lbl: ImageLabel):
    from . import CellFrame
    self: CellFrame

    nl = list(self.mapped_imgs)
    nl.remove(img_lbl)
    self._delete_images(nl)


def _delete_images(self, img_lbls: list[ImageLabel] | ImageLabel) -> None:
    from . import CellFrame
    self: CellFrame

    if not isinstance(img_lbls, list):
        img_lbls = [img_lbls]
    for img_lbl in img_lbls:
        assert img_lbl in self.mapped_imgs, f'{img_lbl=}'

        self.mapped_imgs.pop(img_lbl)
        img_lbl.grid_forget()

    if not len(self.mapped_imgs):
        self._fill_empty_cell()
    else:
        self._reorganize_layout()


def _delete_all_images(self):
    from . import CellFrame
    self: CellFrame

    for img_lbl in list(self.mapped_imgs):
        self.mapped_imgs.pop(img_lbl)
        img_lbl.grid_forget()


def _reorganize_layout(self):
    from . import CellFrame
    self: CellFrame

    new_max_side = ceil(sqrt(len(self.mapped_imgs)))
    for i, img_lbl in enumerate(self.mapped_imgs):
        row, col = i // new_max_side, i % new_max_side
        img_lbl.grid(row=row, column=col)

    if new_max_side != self.max_side:
        self.max_side = new_max_side
        self._update_image_size()


def _update_image_size(self):
    from . import CellFrame
    self: CellFrame

    if self.max_side == 0:
        return

    new_size = int(self.cell_size / self.max_side)
    if new_size != self.img_size:
        for img_lbl in self.mapped_imgs:
            img_lbl.resize_image(new_size)

        self.img_size = new_size


def _fill_empty_cell(self):
    from . import CellFrame
    self: CellFrame

    self.configure(fg_color='gray30', cursor='X_cursor', corner_radius=10)
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)
    puff_lbl = ctk.CTkLabel(self, text='Puffed!', font=(None, 11))
    puff_lbl.grid(row=0, column=0, padx=2, pady=2)


def _undo_fill_empty_cell(self):
    from . import CellFrame
    self: CellFrame

    assert len(self.grid_slaves(row=0, column=0)) > 0, 'Puff label does not exist'
    self.configure(fg_color='gray20', cursor='arrow', corner_radius=0)
    self.rowconfigure(0, weight=0)
    self.columnconfigure(0, weight=0)
    self.grid_slaves(row=0, column=0)[0].grid_forget()
