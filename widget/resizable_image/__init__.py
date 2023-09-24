import tkinter as tk

from PIL import ImageTk
from PIL.Image import Image
from PIL.ImageTk import PhotoImage

from .resize_handler import frm_resize_handler


class ResizableImage(tk.Label):
    resize_threshold = 5

    def __init__(self, src_image: Image, img: Image, img_tk: PhotoImage, *args, **kwargs):
        super().__init__(borderwidth=0, *args, **kwargs)

        self.src_image: Image = src_image
        self.resized_img: Image = img
        self.resized_img_tk: ImageTk = img_tk

        self.grid_propagate(False)
