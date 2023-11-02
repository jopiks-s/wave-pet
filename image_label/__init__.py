from tkinter import Misc

import customtkinter as ctk


class ImageLabel(ctk.CTkLabel):
    def __init__(self, master: Misc, width: int, height: int, image: ctk.CTkImage):
        super().__init__(master, width, height, 0, fg_color='transparent', text='', image=image)
        self.grid_propagate(False)

    def resize_image(self, size: int):
        self.configure(width=size, height=size)
        self.cget('image').configure(size=(size, size))
