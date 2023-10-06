import tkinter as tk
from map import Map

w, h = 600, 600
root = tk.Tk()
root.title('WFC')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.geometry(f'{w}x{h}')
root.resizable(False, False)

map_frm = Map(3, 'tiles/road', master=root, width=w, height=h)
map_frm.grid(row=0, column=0, sticky='nsew')

root.mainloop()
