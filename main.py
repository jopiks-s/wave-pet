import tkinter

import customtkinter
import customtkinter as ctk

from map import Map

customtkinter.deactivate_automatic_dpi_awareness()

root = ctk.CTk()
root.title('WFC')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
s_w, s_h = root.winfo_screenwidth(), root.winfo_screenheight()
w, h = 600, 700
x, y = int((s_w / 2) - (w / 2)), int((s_h / 2) - (h / 2))
root.geometry(f'{w}x{h}+{x}+{y}')
root.resizable(False, False)

map_frm = Map(root, 'tiles/road', 10, w, h)
map_frm.grid(row=0, column=0, sticky='nsew')

root.mainloop()
