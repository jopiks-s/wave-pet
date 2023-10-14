from math import ceil, sqrt

from PIL import Image

from . import ImageLabel, tk


def handle_image_click(self, e: tk.Event):
    from . import CellFrame
    self: CellFrame
    assert isinstance(e.widget, ImageLabel)

    # [TODO] add a handler when clicked and cell is already collapsed
    if len(self.mapped_imgs) == 1:
        assert self.state == CellFrame.State.Collapsed
        return

    self.collapse_cell(e.widget)
    self.tile_set.propagate_collapse(self)


def select_image(self, img_lbl: ImageLabel):
    from . import CellFrame
    self: CellFrame

    nl = list(self.mapped_imgs)
    nl.remove(img_lbl)
    self.delete_images(nl)


def delete_images(self, img_lbls: list[ImageLabel] | ImageLabel) -> None:
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

    cell_size = min(self.winfo_width(), self.winfo_height())
    new_size = int(cell_size / self.max_side)
    if new_size != self.img_size:
        for img_lbl in self.mapped_imgs:
            img_lbl.resized_img = img_lbl.src_image.resize((new_size, new_size), Image.LANCZOS)

        self.img_size = new_size


def _fill_empty_cell(self):
    from . import CellFrame
    self: CellFrame

    self['cursor'] = 'X_cursor'
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)
    puff_lbl = tk.Label(self, text='Puffed!', fg='white', bg='black')
    puff_lbl.grid(row=0, column=0)
