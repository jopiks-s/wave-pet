from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Container
from textual.screen import ModalScreen
from textual.widgets import Button

from text_wfc.tile_pack import TextTilePack
from .wfc import Cell


class TilePicker(ModalScreen[str | None]):
    DEFAULT_CSS = """
        TilePicker {
            align: center middle;
        }
        
        #tile_dialog {
            width: auto;
            height: auto;
            padding: 0 1;
            border: round $secondary;
            background: $surface;
        }

        #tile_actions {
            height: auto;
            width: auto;
        }

        #tile_actions Button {
            min-width: 6;
            margin: 0 1;
        }

        #tile_actions Button:focus {
            background: $accent;
            color: $text;
            text-style: bold;
        }
        """

    BINDINGS = [
        Binding("left", "carousel_focus(-1)", "Previous"),
        Binding("right", "carousel_focus(1)", "Next"),
        Binding("q", "cancel", "Cancel"),
        Binding("esc", "cancel", "Cancel"),
    ]

    def __init__(self, cell: Cell):
        super().__init__()
        self.cell = cell
        self.tile_pack: TextTilePack = cell.tile_pack

    def compose(self) -> ComposeResult:
        with Container(id='tile_dialog'):
            with Horizontal(id="tile_actions"):
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

    def action_carousel_focus(self, direction: int):
        buttons = list(self.query(Button))
        focused = self.focused
        if focused not in buttons:
            buttons[0].focus()
            return

        index = buttons.index(focused)
        buttons[(index + direction) % len(buttons)].focus()
