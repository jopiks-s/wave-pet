import math
import tkinter as tk


class Root(tk.Tk):
    resize_threshold = 250

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prev_w, self.prev_h, self.prev_x, self.prev_y = None, None, None, None
        self.prev_state: str = self.state()
        self.bind('<Configure>', self.resize_handler)

    def resize_handler(self, e: tk.Event):
        if not isinstance(e.widget, tk.Tk):
            return

        def padding_reset_traverse(w: tk.Tk | tk.Widget):
            for el in w.grid_slaves():
                if isinstance(el, tk.Frame):  # todo : replace tk.Frame
                    el.grid(padx=0, pady=0)

                padding_reset_traverse(el)

        if self.prev_state == 'zoomed' and self.state() == 'normal':
            padding_reset_traverse(self)
        elif all((self.prev_w, self.prev_h)) and \
                abs(self.prev_w - e.width) + abs(self.prev_h - e.height) > self.resize_threshold:
            padding_reset_traverse(self)

        self.prev_w = e.width
        self.prev_h = e.height
        self.prev_x = self.winfo_x()
        self.prev_y = self.winfo_y()
        self.prev_state = self.state()
