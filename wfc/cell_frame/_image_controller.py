from math import ceil, sqrt

from PIL import Image

from . import ImageLabel


def delete_images(self, img_lbls: list[ImageLabel]):
    from . import CellFrame
    self: CellFrame

    for img_lbl in img_lbls:
        assert img_lbl in self.mapped_imgs, print(img_lbl)

        self.mapped_imgs.pop(img_lbl)
        img_lbl.grid_forget()

    self.reorganize_layout()


def reorganize_layout(self):
    from . import CellFrame
    self: CellFrame

    self.max_side = ceil(sqrt(len(self.mapped_imgs)))
    for i, img_lbl in enumerate(self.mapped_imgs):
        row, col = i // self.max_side, i % self.max_side
        img_lbl.grid(row=row, column=col)

    self.update_image_size()


def update_image_size(self):
    from . import CellFrame
    self: CellFrame

    cell_size = min(self.winfo_width(), self.winfo_height())
    new_size = int(cell_size / self.max_side)
    if new_size != self.img_size:
        for img_lbl in self.mapped_imgs:
            img_lbl.resized_img = img_lbl.src_image.resize((new_size, new_size), Image.LANCZOS)

        self.img_size = new_size
