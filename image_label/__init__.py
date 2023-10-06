import tkinter as tk

from PIL import ImageTk
from PIL.Image import Image
from PIL.ImageTk import PhotoImage


class ImageLabel(tk.Label):
    def __init__(self, src_image: Image, img: Image, img_tk: PhotoImage, *args, **kwargs):
        super().__init__(*args, borderwidth=0, **kwargs)

        self.src_image: Image = src_image
        self.resized_img: Image = img
        self.resized_img_tk: ImageTk = img_tk
        self.grid_propagate(False)
