import tkinter as tk

import wfc
from ._resize import AfterResizingEvent


class AspectFrame(tk.Frame):
    from ._resize import resize_handler, bind_after_resizing, after_resizing_handler
    from ._images_control import set_image_size

    def __init__(self, aspect_ratio: float, *args, **kwargs):
        super().__init__(borderwidth=0, *args, **kwargs)
        self.bind('<Configure>', self.resize_handler)
        self.grid_propagate(False)

        self.aspect_ratio = aspect_ratio
        self.after_resizing_pool = []
        self.wfc_cell: wfc.Cell = None
