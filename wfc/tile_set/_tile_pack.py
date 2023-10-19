from PIL import Image, ImageTk


def __len__(self):
    return len(self.tile_pack)


def items(self):
    return self.tile_pack.items()


def values(self):
    return self.tile_pack.values()


def resize_pack(self, size: int) -> dict[str, tuple[Image.Image, ImageTk.PhotoImage]]:
    scaled_imgs = {}
    for name, tile in self.items():
        resized_img = tile.image.resize((size, size), Image.LANCZOS)
        scaled_imgs[name] = (resized_img, ImageTk.PhotoImage(resized_img))

    return scaled_imgs


# todo: move to 'board' class
def get_coords(self, row: int, column: int, direction) -> tuple[int, int] | tuple[None, None]:
    from . import TileSet, Tile
    self: TileSet
    direction: Tile.Directions

    match direction:
        case Tile.Directions.UP:
            row -= 1
        case Tile.Directions.RIGHT:
            column += 1
        case Tile.Directions.DOWN:
            row += 1
        case Tile.Directions.LEFT:
            column -= 1

    board_dimension = self.map_frm.board_dimension
    if 0 <= row < board_dimension and 0 <= column < board_dimension:
        return row, column

    return None, None
