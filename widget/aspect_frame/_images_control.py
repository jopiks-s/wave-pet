from PIL import Image, ImageTk


def set_image_size(self, new_size: int):
    from widget.resizable_image import ResizableImage
    self.wfc_cell.img_size = new_size
    for resizable_lbl in [w for w in self.grid_slaves() if isinstance(w, ResizableImage)]:
        resizable_lbl.resized_img = resizable_lbl.src_image.resize((new_size, new_size), Image.LANCZOS)
        resizable_lbl.resized_img_tk = ImageTk.PhotoImage(resizable_lbl.resized_img)
        resizable_lbl['image'] = resizable_lbl.resized_img_tk
