from copy import copy

from textual.app import ComposeResult
from textual.containers import Horizontal, Container
from textual.coordinate import Coordinate
from textual.screen import ModalScreen
from textual.widgets import DataTable, Button, Input, Label

from .status_line import StatusLine
from .tile_picker import TilePicker
from .wfc import Cell, Board


class MapSizeModal(ModalScreen[int | None]):
    CSS = """
    MapSizeModal {
        align: center middle;
    }
    
    #size_dialog {
        width: auto;
        height: auto;
        padding: 1 2;
        border: round $accent;
        background: $surface;
    }
    
    #size_title {
        text-style: bold;
    }
    
    #size_actions {
        height: auto;
        width: auto;
    }
    
    #size_input {
        width: 16;
    }
    
    #size_actions Button {
        min-width: 12;
        margin: 0 1;
    }
    """

    def __init__(self, current_size: int):
        super().__init__()
        self.current_size = current_size

    def compose(self) -> ComposeResult:
        with Container(id='size_dialog'):
            yield Label("Board size", id="size_title")
            with Horizontal(id="size_actions"):
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
            return
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


class Map(DataTable[Cell]):
    def __init__(self, board: Board, status_line: StatusLine, *args, **kwargs):
        super().__init__(show_header=False, *args, **kwargs)
        self.board = board
        self.status_line = status_line

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
        self.status_line.update_status()

    def reset(self):
        self.board.reset()
        self._render_rows()
        self.status_line.update_status()

    def change_size(self):
        def handle(new_size: int | None) -> None:
            if new_size is None:
                return

            self.board.change_size(new_size)
            self._render_rows()
            self.status_line.update_status()

        self.app.push_screen(MapSizeModal(self.board.size), handle)

    def update_cells(self, changed_cells: set[Cell]):
        for changed_cell in changed_cells:
            changed_cell.highlighted = True
            self.update_cell_at(Coordinate(*changed_cell.coordinates), changed_cell)

        self.app.lock()
        self.set_timer(.3, lambda: self.clear_highlights(changed_cells))

    def clear_highlights(self, changed_cells: set[Cell]):
        self.app.unlock()
        for changed_cell in changed_cells:
            changed_cell.highlighted = False
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
            self.status_line.update_status()

        self.app.push_screen(TilePicker(cell), handle_pick)
