import tkinter


def _on_enter(self, e: tkinter.Event):
    if e.state != 0:
        return
    self.hover = True
    self.resize_image(self.size + self.hover_add_amount, True)


def _on_leave(self, e: tkinter.Event):
    if e.state != 0:
        return
    self.hover = False
    self.resize_image(self.size - self.hover_add_amount, True)


def _on_press(self, e: tkinter.Event):
    self.resize_image(self.size + self.press_add_amount, True)


def _on_release(self, e: tkinter.Event):
    self.resize_image(self.size - self.press_add_amount, True)
