from pathlib import Path

from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, DataTable, Footer, Header, Static

from abc_wfc import Board
from abc_wfc.cell import Cell
from text_wfc.tile_pack import TextTilePack


class TilePicker(ModalScreen[str | None]):
    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def __init__(self, cell: Cell, tile_pack: TextTilePack):
        super().__init__()
        self.cell = cell
        self.tile_pack = tile_pack

    def compose(self) -> ComposeResult:
        yield Static(
            f"Choose tile for ({self.cell.row}, {self.cell.column})",
            id="tile-picker-title",
        )
        with Horizontal(id="tile-picker-options"):
            for tile_name in sorted(self.cell.tiles):
                symbol = str(self.tile_pack[tile_name])
                yield Button(symbol, id=tile_name)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id)

    def action_cancel(self) -> None:
        self.dismiss(None)


class CellView:
    def __init__(self, cell: Cell, tile_pack: TextTilePack):
        self.cell = cell
        self.tile_pack = tile_pack

    def __rich__(self) -> Text:
        entropy = self.cell.entropy
        if entropy == 0:
            return Text("X", style="bold red")
        if entropy == 1:
            symbol = str(self.tile_pack[self.cell.collapsed_tile])
            return Text(symbol, style="bold green")
        return Text(str(entropy), style="yellow")


class Map(DataTable[CellView]):
    def __init__(self, board: Board, tile_pack: TextTilePack, *args, **kwargs):
        super().__init__(show_header=False, *args, **kwargs)
        self.board = board
        self.tile_pack = tile_pack
        self.cursor_type = "cell"
        self.cell_padding = 0
        self.add_columns(*[""] * board._size)
        self.add_rows(self._render_rows())

    def _render_rows(self) -> list[list[CellView]]:
        return [
            [CellView(cell, self.tile_pack) for cell in row]
            for row in self.board._board
        ]

    def refresh_board(self) -> None:
        for row_index, row in enumerate(self.board._board):
            for column_index, cell in enumerate(row):
                self.update_cell_at((row_index, column_index), CellView(cell, self.tile_pack))

    def is_solved(self) -> bool:
        return all(cell.entropy == 1 for row in self.board._board for cell in row)

    def on_data_table_cell_selected(self, event: DataTable.CellSelected) -> None:
        row, column = event.coordinate
        cell = self.board.get_cell(row, column)

        if cell.entropy == 0:
            self.notify("This cell is broken and cannot be collapsed.", severity="error")
            return

        if cell.entropy == 1:
            self.notify("This cell is already collapsed.")
            return

        def apply_choice(tile_name: str | None) -> None:
            if tile_name is None:
                self.notify("Tile selection canceled.")
                return

            cell.tiles = {tile_name}
            self.board.propagate_collapse(cell)
            self.refresh_board()

            if self.board.is_broken():
                self.notify("Propagation produced an invalid board.", severity="error")
            elif self.is_solved():
                self.notify("Board solved.", severity="information")
            else:
                self.notify(f"Collapsed cell at ({row}, {column}) with {tile_name}.")

        self.app.push_screen(TilePicker(cell, self.tile_pack), apply_choice)


class WfcApp(App):
    CSS = """
    TilePicker {
        align: center middle;
    }

    #tile-picker-title {
        background: $surface;
        color: $text;
        padding: 1 2 0 2;
    }

    #tile-picker-options {
        background: $surface;
        padding: 0 2 1 2;
        border: round $accent;
        width: auto;
        height: auto;
    }

    #tile-picker-options Button {
        min-width: 5;
        margin: 0 1 0 0;
    }
    """
    BINDINGS = [
        Binding("r", "reset_board", "Reset"),
        Binding("s", "solve_board", "Solve"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self, board_size: int = 15):
        super().__init__()
        tiles_path = Path(__file__).resolve().parent.parent / "text_wfc" / "tiles" / "road"
        self.tile_pack = TextTilePack(str(tiles_path))
        self.board = Board(board_size, self.tile_pack)

    def compose(self) -> ComposeResult:
        yield Header(name="WFC")
        yield Map(self.board, self.tile_pack)
        yield Footer()

    def action_reset_board(self) -> None:
        self.board.reset()
        self.query_one(Map).refresh_board()
        self.notify("Board reset.")

    def action_solve_board(self) -> None:
        if self.board.is_broken():
            self.notify("Reset the board before solving.", severity="warning")
            return

        self.board.solve()
        self.query_one(Map).refresh_board()
        self.notify("Board solved.")


if __name__ == "__main__":
    WfcApp().run()
