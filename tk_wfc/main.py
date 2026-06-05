from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import customtkinter as ctk

from abc_wfc import AbcTile, AbcTilePack, Board, Directions
from abc_wfc.cell import Cell

PACKS_DIR = Path(__file__).parent.parent / 'tile_packs' / 'image'
IMAGE_EXTENSIONS = (".png",)


@dataclass(frozen=True)
class TkTile(AbcTile):
    image_path: Path = Path()


class TkTilePack(AbcTilePack):
    def __init__(self, folder: Path):
        self.folder = folder
        super().__init__(folder)

    def load_tile(self, tile_name: str, content: list[Any]) -> TkTile:
        rules = {Directions[d]: set(tiles) for d, tiles in content[0].items()}
        for ext in IMAGE_EXTENSIONS:
            if (path := self.folder / f"{tile_name}{ext}").exists():
                return TkTile(tile_name, rules, path)
        raise FileNotFoundError(f"Missing image for tile '{tile_name}' in {self.folder}")


class WfcApp(ctk.CTk):
    min_size = 4
    max_size = 40

    def __init__(self) -> None:
        super().__init__()
        self.title("WFC")
        self.geometry("980x820")
        self.minsize(820, 700)

        self.pack_paths = self._find_packs()
        if not self.pack_paths:
            raise RuntimeError(f"No image tile packs found in {PACKS_DIR}")

        self.pack_var = tk.StringVar(value=next(iter(self.pack_paths)))
        self.size_var = tk.StringVar(value="17")
        self.speed_var = tk.IntVar(value=40)
        self.autorun = False
        self.cell_size = 1
        self.source_images: dict[str, tk.PhotoImage] = {}
        self.tile_images: dict[tuple[str, int], tk.PhotoImage] = {}

        self._build_layout()
        self._load_board()

    def _build_layout(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 8))
        controls.grid_columnconfigure(9, weight=1)

        ctk.CTkLabel(controls, text="Tile pack").grid(row=0, column=0, padx=(0, 6))
        ctk.CTkOptionMenu(
            controls,
            values=list(self.pack_paths),
            variable=self.pack_var,
            command=lambda _: self._load_board(),
            width=140,
        ).grid(row=0, column=1, padx=(0, 16))

        ctk.CTkLabel(controls, text="Size").grid(row=0, column=2, padx=(0, 6))
        size_entry = ctk.CTkEntry(controls, width=50, textvariable=self.size_var)
        size_entry.grid(row=0, column=3, padx=(0, 16))
        for event in ("<Return>", "<FocusOut>"):
            size_entry.bind(event, lambda _: self._load_board())

        ctk.CTkLabel(controls, text="Delay").grid(row=0, column=4, padx=(0, 6))
        ctk.CTkSlider(
            controls, from_=5, to=250, variable=self.speed_var, width=150,
        ).grid(row=0, column=5, padx=(0, 16))

        ctk.CTkButton(controls, text="Step", width=70, command=self.step).grid(row=0, column=6, padx=(0, 8))
        self.run_button = ctk.CTkButton(controls, text="Run", width=70, command=self.toggle_run)
        self.run_button.grid(row=0, column=7, padx=(0, 8))
        ctk.CTkButton(controls, text="Solve", width=70, command=self.solve).grid(row=0, column=8, padx=(0, 8))
        ctk.CTkButton(controls, text="Reset", width=70, command=self._load_board).grid(row=0, column=9, sticky="w")

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(body, background="#202124", highlightthickness=0, bd=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", lambda _: self.draw())

        self.status = ctk.CTkLabel(body, anchor="w")
        self.status.grid(row=1, column=0, sticky="ew", pady=(8, 0))

    @staticmethod
    def _find_packs() -> dict[str, Path]:
        if not PACKS_DIR.exists():
            return {}
        return {
            path.parent.name: path.parent
            for path in sorted(PACKS_DIR.glob("*/ruleset.json"))
        }

    def _set_run_mode(self, running: bool) -> None:
        self.autorun = running
        self.run_button.configure(text="Pause" if running else "Run")

    def _load_board(self) -> None:
        self._set_run_mode(False)

        try:
            size = int(self.size_var.get())
        except ValueError:
            size = 18
        size = max(self.min_size, min(self.max_size, size))
        self.size_var.set(str(size))

        self.tile_pack = TkTilePack(self.pack_paths[self.pack_var.get()])
        self.board = Board(size, self.tile_pack)
        self.source_images = {
            name: tk.PhotoImage(file=tile.image_path)
            for name, tile in self.tile_pack.items()
        }
        self.tile_images.clear()
        self.draw()

    def toggle_run(self) -> None:
        self._set_run_mode(not self.autorun)
        if self.autorun:
            self.after(0, self._run_next_step)

    def _run_next_step(self) -> None:
        if not self.autorun:
            return
        self.step()
        if self.autorun and not self.board.solved:
            self.after(self.speed_var.get(), self._run_next_step)
        else:
            self._set_run_mode(False)

    def step(self) -> None:
        if not self.board.solved:
            if cell := self.board.choose_cell():
                cell.collapse()
                self.board.propagate_collapse(cell)
        self.draw()

    def solve(self) -> None:
        self._set_run_mode(False)
        if not self.board.solved:
            self.board.solve()
        self.draw()

    def draw(self) -> None:
        self.canvas.delete("all")

        width = max(1, self.canvas.winfo_width())
        height = max(1, self.canvas.winfo_height())
        grid_size = min(width, height)
        offset_x = (width - grid_size) // 2
        offset_y = (height - grid_size) // 2
        self.cell_size = grid_size / self.board.size

        for row in range(self.board.size):
            for col in range(self.board.size):
                x0 = offset_x + col * self.cell_size
                y0 = offset_y + row * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                self._draw_cell(self.board.get_cell(row, col), x0, y0, x1, y1)

        self._update_status()

    def _draw_cell(self, cell: Cell, x0: float, y0: float, x1: float, y1: float) -> None:
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        self.canvas.create_rectangle(
            x0, y0, x1, y1, fill=self._cell_fill(cell), outline="#2f3338", width=1,
        )

        if cell.entropy == 1:
            size = max(1, int(self.cell_size))
            self.canvas.create_image(cx, cy, image=self._tile_image(cell.collapsed_tile, size))
        elif self.cell_size >= 18:
            self.canvas.create_text(
                cx, cy,
                text="!" if cell.entropy == 0 else str(cell.entropy),
                fill="#ffffff" if cell.entropy > 0 else "#ffe7e7",
                font=("Segoe UI", max(8, int(self.cell_size * 0.32)), "bold"),
            )

    def _cell_fill(self, cell: Cell) -> str:
        match cell.entropy:
            case 0:
                return "#d94848"
            case 1:
                return "#101214"
            case _:
                shade = 35 + round((cell.entropy / self.tile_pack.size) * 50)
                return f"#{shade:02x}{shade:02x}{shade:02x}"

    def _tile_image(self, tile_name: str, size: int) -> tk.PhotoImage:
        key = (tile_name, size)
        if key in self.tile_images:
            return self.tile_images[key]

        source = self.source_images[tile_name]
        source_size = max(source.width(), source.height(), 1)
        if source_size < size:
            scale = max(1, round(size / source_size))
            image = source.zoom(scale, scale)
        elif source_size > size:
            scale = max(1, round(source_size / size))
            image = source.subsample(scale, scale)
        else:
            image = source.copy()

        self.tile_images[key] = image
        return image

    def _update_status(self) -> None:
        broken = self.board.is_broken()
        if self.board.solved:
            message = "Finished with contradictions." if broken else "Solved."
        elif broken:
            message = "Solving (contradictions present)."
        else:
            message = "Ready."

        total = self.board.size ** 2
        self.status.configure(
            text=(
                f"{message} Pack: {self.tile_pack.name} | "
                f"Collapsed: {self.board.solved_count}/{total} | "
                f"Tiles: {self.tile_pack.size}"
            )
        )


if __name__ == "__main__":
    ctk.deactivate_automatic_dpi_awareness()
    WfcApp().mainloop()
