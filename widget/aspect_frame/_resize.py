import tkinter as tk
from typing import Callable


class AfterResizingEvent:
    def __init__(self, widget, new_w, new_h, new_padx, new_pady):
        self.widget = widget
        self.new_w = new_w
        self.new_h = new_h
        self.new_padx = new_padx
        self.new_pady = new_pady


def resize_handler(self, e: tk.Event) -> None:
    padx, pady = self.grid_info()['padx'], self.grid_info()['pady']
    new_w, new_h, new_padx, new_pady = e.width, e.height, padx, pady
    full_w, full_h = e.width + (padx * 2), e.height + (pady * 2)
    if not e.width or not e.height:
        new_aspect = 0
    else:
        new_aspect = e.width / e.height

    if abs(new_aspect - self.aspect_ratio) > 0.01:
        if not full_w or not full_h:
            new_padx = 0
            new_pady = 0
        else:
            full_aspect = full_w / full_h
            if full_aspect > self.aspect_ratio:
                new_w = int(full_h * self.aspect_ratio)
                new_padx = int((full_w - new_w) / 2)
                new_pady = 0
            elif full_aspect < self.aspect_ratio:
                new_h = int(full_w / self.aspect_ratio)
                new_pady = int((full_h - new_h) / 2)
                new_padx = 0
            else:
                new_padx = 0
                new_pady = 0

    if padx == new_padx and pady == new_pady:
        return

    from . import AspectFrame
    for w in self.master.grid_slaves():
        if isinstance(w, AspectFrame):
            w.grid(padx=new_padx, pady=new_pady)

    self.after_resizing_handler(AfterResizingEvent(self, new_w, new_h, new_padx, new_pady))


def bind_after_resizing(self, func: Callable[[AfterResizingEvent], None]):
    self.after_resizing_pool.append(func)


def after_resizing_handler(self, e: AfterResizingEvent):
    for f in self.after_resizing_pool:
        f(e)
