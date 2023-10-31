import customtkinter as ctk


class ImageLabel(ctk.CTkLabel):
    def __init__(self, image: ctk.CTkImage, *args, **kwargs):
        super().__init__(*args, text='', corner_radius=0, image=image, **kwargs)
        self.grid_propagate(False)

    def resize_image(self, size: int):
        self.configure(width=size, height=size)
        self.cget('image').configure(size=(size, size))
