from widget.root import Root
from map import Map

root = Root()
root.title('WFC')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.geometry('500x500')

map_frm = Map(3, 100, 'tiles/road', master=root)
map_frm.grid(row=0, column=0, sticky='nsew')

root.mainloop()
