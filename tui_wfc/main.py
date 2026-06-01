from copy import copy
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.coordinate import Coordinate
from textual.screen import ModalScreen
from textual.widgets import DataTable, Footer, Header, Button, Input

from text_wfc.tile_pack import TextTilePack
from wfc import Cell, Board

SIZE = 15
PACK = 'forrest-sea'
TILES_PATH = Path(__file__).parent.parent / 'tiles' / 'text' / PACK


class MapSizeModal(ModalScreen[int | None]):
    BINDINGS = [
        Binding("q", "cancel", "Cancel"),
        Binding("esc", "cancel", "Cancel"),
    ]

    def __init__(self, current_size: int):
        super().__init__()
        self.current_size = current_size

    def compose(self) -> ComposeResult:
        yield Input('', str(self.current_size), type='integer', id="size_input")
        yield Button("Apply", 'success', id="apply")
        yield Button("Cancel", 'error', id="cancel")

    def validate(self, value: str) -> int | None:
        input_widget = self.query_one(Input)
        if value == '' and input_widget.placeholder:
            return self.validate(input_widget.placeholder)

        try:
            value = int(value)
            if value == 0:
                raise ValueError
            return abs(value)
        except (TypeError, ValueError):
            return None

    def submit(self) -> None:
        input_widget = self.query_one(Input)
        value = self.validate(input_widget.value)
        if value is None:
            self.notify(f'Invalid input: {input_widget.value}', severity="error")
        self.dismiss(value)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.submit()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'apply':
            self.submit()
            return
        elif event.button.id == "cancel":
            self.dismiss(None)
            return

    def action_cancel(self):
        self.dismiss(None)


class TilePicker(ModalScreen[str | None]):
    BINDINGS = [
        Binding("q", "cancel", "Cancel"),
        Binding("esc", "cancel", "Cancel"),
    ]

    # CSS = """
    # Button {
    #     background: green;
    # }
    # """

    def __init__(self, cell: Cell):
        super().__init__()
        self.cell = cell
        self.tile_pack: TextTilePack = cell.tile_pack

    def compose(self) -> ComposeResult:
        for tile_name in sorted(self.cell.tiles):
            symbol = self.tile_pack[tile_name].symbol
            yield Button(symbol, id=tile_name)
        yield Button('X', variant='error', id='close_button')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'close_button':
            self.dismiss()
            return
        self.dismiss(event.button.id)

    def action_cancel(self):
        self.dismiss()


class Map(DataTable[Cell]):
    def __init__(self, board_size: int, tile_pack: TextTilePack, *args, **kwargs):
        super().__init__(show_header=False, *args, **kwargs)
        self.tile_pack = tile_pack
        self.board = Board(board_size, tile_pack)

        self.cell_padding = 0
        self.cursor_type = "cell"
        self._render_rows()

    def _render_rows(self):
        if len(self.columns) != self.board.size:
            for column in copy(self.columns):
                self.remove_column(column)
            for _ in range(self.board.size):
                self.add_column('', width=2)

        for row in copy(self.rows):
            self.remove_row(row)
        self.add_rows(self.board._board)

    def solve(self):
        if self.board.solved:
            self.board.reset()
        self.board.solve()
        self._render_rows()

    def reset(self):
        self.board.reset()
        self._render_rows()

    def change_size(self):
        def handle(new_size: int | None) -> None:
            if new_size is None:
                return

            self.board.change_size(new_size)
            self._render_rows()

        self.app.push_screen(MapSizeModal(self.board.size), handle)

    def update_cells(self, changed_cells: set[Cell]):
        for changed_cell in changed_cells:
            self.update_cell_at(Coordinate(*changed_cell.coordinates), changed_cell)

    def on_data_table_cell_selected(self, event: DataTable.CellSelected) -> None:
        cell: Cell = event.value

        if cell.entropy == 0:
            self.notify("This cell is broken and cannot be collapsed.", severity="warning")
            return
        elif cell.entropy == 1:
            self.notify("This cell is already collapsed.")
            return

        def handle_pick(tile: str | None):
            if tile is None:
                return
            cell.collapse(tile)
            changes = self.board.propagate_collapse(cell)
            changes.add(cell)
            self.update_cells(changes)

            self.notify(f'{event.coordinate} collapsed!')

        self.app.push_screen(TilePicker(cell), handle_pick)


class WfcApp(App):
    BINDINGS = [
        Binding("r", "reset_board", "Reset"),
        Binding("s", "solve_board", "Solve"),
        Binding("q", "quit", "Quit"),
        Binding("b", "change_size", "Size"),
    ]

    def __init__(self, tiles_path: Path):
        super().__init__()
        self.tiles_path = tiles_path
        self.tile_pack = TextTilePack(tiles_path)

    def compose(self) -> ComposeResult:
        yield Header(name="Wave Function Collapse")
        yield Map(SIZE, self.tile_pack)
        yield Footer()

    def action_reset_board(self) -> None:
        self.query_one(Map).reset()

    def action_solve_board(self) -> None:
        self.query_one(Map).solve()

    def action_change_size(self) -> None:
        self.query_one(Map).change_size()


if __name__ == "__main__":
    WfcApp(TILES_PATH).run()
