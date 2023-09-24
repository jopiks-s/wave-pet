import json
import math
import os
import tkinter as tk

from PIL import ImageTk, Image

from widget.aspect_frame import AspectFrame
from widget.resizable_image import ResizableImage, frm_resize_handler


class Tile:
    def __init__(self, name: str, rules: list[list[str]], img: Image.Image):
        self.name = name
        self.rules = rules
        self.image = img


class TileSet:
    def __init__(self, path: str):
        rules_path = f'{path}/set_rules.json'
        assert os.path.exists(rules_path), f'Path to rules file: {rules_path}'

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
        self.board: list[list] = None

    def propagate_collapse(self, row, column):
        ...


class Cell:
    def __init__(self, container: AspectFrame, tile_set: TileSet, mapped_tiles: dict[ResizableImage, Tile],
                 img_size: int):
        self.container = container
        self.tile_set = tile_set
        self.mapped_tiles = mapped_tiles
        self.img_size = img_size
        self.max_side = tile_set.board_dim

    def select_image(self, name):
        ...

    def update_cell(self, constraints):
        ...

    def delete_image(self, img_lbl: ResizableImage):
        ...


def create_map_layout(widget: tk.Frame, tile_set: TileSet, map_size: int, cell_size: int):
    img_size = int(cell_size / tile_set.board_dim)
    scaled_imgs = {name: tile.image.resize((img_size, img_size), Image.LANCZOS)
                   for name, tile in tile_set.tile_pack.items()}
    for k in scaled_imgs:
        scaled_imgs[k] = (scaled_imgs[k], ImageTk.PhotoImage(scaled_imgs[k]))

    tile_set.board = []
    for i in range(map_size):
        tile_set.board.append([])
        for j in range(map_size):
            asp_frm = AspectFrame(1.0, master=widget)
            asp_frm.rowconfigure(tuple(range(tile_set.board_dim)), weight=1)
            asp_frm.columnconfigure(tuple(range(tile_set.board_dim)), weight=1)
            asp_frm.grid(row=i, column=j, sticky='nsew')
            asp_frm.bind_after_resizing(frm_resize_handler)
            mapped_tiles = {}
            for k, tile in enumerate(tile_set.tile_pack.values()):
                row, col = k // tile_set.board_dim, k % tile_set.board_dim
                img, img_tk = scaled_imgs[tile.name]
                img_lbl = ResizableImage(tile.image, img, img_tk, master=asp_frm, image=img_tk)
                img_lbl.grid(row=row, column=col, sticky='nsew')
                mapped_tiles[img_lbl] = tile

            asp_frm.wfc_cell = Cell(asp_frm, tile_set, mapped_tiles, img_size)
            tile_set.board[i].append(asp_frm.wfc_cell)
