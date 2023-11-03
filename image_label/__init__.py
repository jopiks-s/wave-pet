from tkinter import Misc

import customtkinter as ctk


class ImageLabel(ctk.CTkLabel):
    from ._on_hover import _on_enter, _on_leave, _on_press, _on_release

    def __init__(self, master: Misc, size: int, image: ctk.CTkImage):
        super().__init__(master, size, size, 0, fg_color='transparent', text='', image=image)
        self.grid_propagate(False)

        self.size = size
        self.hover_add_amount = 5
        self.press_add_amount = 2
        self.hover = False
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<ButtonPress-1>', self._on_press)
        self.bind('<ButtonRelease-1>', self._on_release)

    def resize_image(self, size: int, by_hover: bool = False):
        if not by_hover and self.hover:
            size += self.hover_add_amount

        self.size = size
        self.configure(width=size, height=size)
        self.cget('image').configure(size=(size, size))
