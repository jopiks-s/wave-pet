from map import Map
from widget.root import Root

root = Root()
root.title('WFC')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.geometry('600x600')

map_frm = Map(3, 70, 'tiles/road', master=root)
map_frm.grid(row=0, column=0, sticky='nsew')

root.mainloop()
