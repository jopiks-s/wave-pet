from PIL import Image, ImageTk


def set_image_size(self, new_size: int):
    from widget.resizable_image import ResizableImage
    self.wfc_cell.img_size = new_size
    for img_lbl in [w for w in self.grid_slaves() if isinstance(w, ResizableImage)]:
        img_lbl.resized_img = img_lbl.src_image.resize((new_size, new_size), Image.LANCZOS)
        img_lbl.resized_img_tk = ImageTk.PhotoImage(img_lbl.resized_img)
        img_lbl['image'] = img_lbl.resized_img_tk


def update_image_size(self):
    cell_size = min(self.winfo_width(), self.winfo_height())
    new_size = int(cell_size / self.wfc_cell.max_side)
    self.set_image_size(new_size)
