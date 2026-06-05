from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.events import MouseEvent
from textual.widgets import Footer, Header

from text_wfc.tile_pack import TextTilePack
from .map import Map
from .status_line import StatusLine
from .wfc import Board

SIZE = 15
PACKS = ['road', 'forrest-sea', 'network']
TILES_PATH = Path(__file__).parent.parent / 'tile_packs' / 'text' / PACKS[1]


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
        self.board = Board(SIZE, self.tile_pack)

    def compose(self) -> ComposeResult:
        yield Header(name="Wave Function Collapse")
        with Container(id="map-container"):
            status_line = StatusLine(self.board)
            _map = Map(self.board, status_line, id="map")
            yield _map
        yield status_line
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
