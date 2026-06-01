from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.events import MouseEvent
from textual.widgets import Footer, Header

from .map import Map
from text_wfc.tile_pack import TextTilePack

SIZE = 15
PACK = ['road', 'forrest-sea'][1]
TILES_PATH = Path(__file__).parent.parent / 'tiles' / 'text' / PACK


class WfcApp(App):
    CSS = """
        #map-container {
            align: center middle;
            height: 1fr;
            width: 100%;
        }

        Map {
            height: auto; 
            width: auto;
        }
        """

    BINDINGS = [
        Binding("r", "reset_board", "Reset"),
        Binding("s", "solve_board", "Solve"),
        Binding("q", "quit", "Quit"),
        Binding("b", "change_size", "Size"),
    ]

    def __init__(self, tiles_path: Path):
        super().__init__()
        self._locked = False

        self.tiles_path = tiles_path
        self.tile_pack = TextTilePack(tiles_path)

    def compose(self) -> ComposeResult:
        yield Header(name="Wave Function Collapse")
        with Container(id="map-container"):
            yield Map(SIZE, self.tile_pack, id="map")
        yield Footer()

    def lock(self):
        self._locked = True

    def unlock(self):
        self._locked = False

    def on_event(self, event: MouseEvent):
        if self._locked and isinstance(event, MouseEvent):
            event._forwarded = True
        return super().on_event(event)

    def on_key(self, event) -> None:
        if self._locked and event.key not in {"q"}:
            event.stop()
            event.prevent_default()

    def action_reset_board(self) -> None:
        self.query_one(Map).reset()

    def action_solve_board(self) -> None:
        self.query_one(Map).solve()

    def action_change_size(self) -> None:
        self.query_one(Map).change_size()


if __name__ == "__main__":
    WfcApp(TILES_PATH).run()
