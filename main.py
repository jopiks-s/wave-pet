import tkinter as tk
from map import Map


def auto(e):
    map_frm.tile_set.auto_solve()


root = tk.Tk()
root.title('WFC')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
s_w, s_h = root.winfo_screenwidth(), root.winfo_screenheight()
w, h = 600, 600
x, y = int((s_w / 2) - (w / 2)), int((s_h / 2) - (h / 2))
root.geometry(f'{w}x{h}+{x}+{y}')
root.resizable(False, False)

map_frm = Map(10, 'tiles/road', master=root, width=w, height=h)
map_frm.grid(row=0, column=0, sticky='nsew')

root.bind('<KeyPress-w>', auto)

root.mainloop()
