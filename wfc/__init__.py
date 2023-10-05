import json
import math
import os
import tkinter as tk
from functools import partial

from PIL import ImageTk, Image

from widget.aspect_frame import AspectFrame
from widget.resizable_image import ResizableImage


class Tile:
    def __init__(self, name: str, rules: list[list[str]], img: Image.Image):
        self.name = name
        self.rules = rules
        self.image = img


class TileSet:
    def __init__(self, path: str):
        rules_path = f'{path}/set_rules.json'
        assert os.path.exists(rules_path), f'Path to rules file: {rules_path}'

        self.board: list[list[Cell]] = None
        self.tile_pack = {}
        with open(rules_path, 'r') as f:
            set_rules = json.load(f)
            for file_name in os.listdir(path):
                if file_name.split('.')[1] not in ('png', 'jpg'):
                    continue

                name = file_name.split('.')[0]
                img = Image.open(f'{path}/{file_name}')
                self.tile_pack[name] = Tile(name, set_rules[name], img)

        self.board_dim = math.ceil(math.sqrt(len(self.tile_pack)))
        self.grid_size = (math.ceil(len(self) / self.board_dim),
                          self.board_dim)

    def __len__(self):
        return len(self.tile_pack)

    def propagate_collapse(self, row, column):
        ...


class Cell:
    def __init__(self, container: AspectFrame, tile_set: TileSet, mapped_imgs: dict[ResizableImage, Tile],
                 img_size: int):
        self.container = container
        self.tile_set = tile_set
        self.mapped_imgs = mapped_imgs
        self.img_size = img_size
        self.max_side = tile_set.board_dim

    def select_image(self, name):
        ...

    def update_cell(self, constraints):
        ...

    def delete_image(self, e: tk.Event):
        img_lbl = e.widget
        assert e.widget in self.mapped_imgs

        row, col = img_lbl.grid_info()['row'], img_lbl.grid_info()['column']
        self.mapped_imgs.pop(img_lbl)
        img_lbl.grid_forget()

        if not len(self.container.grid_slaves(row=row)):
            self.container.rowconfigure(row, weight=0, minsize=0)
        if not len(self.container.grid_slaves(column=col)):
            self.container.columnconfigure(col, weight=0, minsize=0)

        real_max_side = -1
        for i in range(self.tile_set.board_dim):
            real_max_side = max(len(self.container.grid_slaves(row=i)), real_max_side)
        for i in range(self.tile_set.board_dim):
            real_max_side = max(len(self.container.grid_slaves(column=i)), real_max_side)

        if self.max_side != real_max_side:
            print(f'{self.max_side=}, {real_max_side=}')
            self.max_side = real_max_side
            self.container.update_image_size()


def create_map_layout(map_frm: tk.Frame, tile_set: TileSet, map_size: int, cell_size: int):
    scaled_imgs = {}
    img_size = int(cell_size / tile_set.board_dim)
    for name, tile in tile_set.tile_pack.items():
        resized_img = tile.image.resize((img_size, img_size), Image.LANCZOS)
        scaled_imgs[name] = (resized_img, ImageTk.PhotoImage(resized_img))

    tile_set.board = []
    for i in range(map_size):
        tile_set.board.append([])
        for j in range(map_size):
            asp_frm = AspectFrame(1.0, master=map_frm, bg='black')
            asp_frm.grid(row=i, column=j, sticky='nsew')
            mapped_imgs = {}
            for k, tile in enumerate(tile_set.tile_pack.values()):
                row, col = k // tile_set.board_dim, k % tile_set.board_dim
                asp_frm.rowconfigure(row, weight=1)
                asp_frm.columnconfigure(col, weight=1)

                img, img_tk = scaled_imgs[tile.name]
                img_lbl = ResizableImage(tile.image, img, img_tk, master=asp_frm, image=img_tk)
                img_lbl.grid(row=row, column=col, sticky='nsew')
                mapped_imgs[img_lbl] = tile
            asp_frm.wfc_cell = Cell(asp_frm, tile_set, mapped_imgs, img_size)
            for img_lbl in mapped_imgs:
                img_lbl.bind('<Button-1>', asp_frm.wfc_cell.delete_image)

            tile_set.board[i].append(asp_frm.wfc_cell)
