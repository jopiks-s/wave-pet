from textual.widgets import Static

from .wfc import Board


class StatusLine(Static):
    DEFAULT_CSS = """
        StatusLine {
            height: 1;
            content-align: center middle;
            color: $text-muted;
            text-style: dim;
        }
    """

    def __init__(self, board: Board):
        super().__init__()
        self.board = board
        self.update_status()

    def update_status(self) -> None:
        tile_pack = self.board.tile_pack.name
        size = self.board.size
        solved = self.board.solved_count
        total = size ** 2
        percent = (solved/total)*100
        self.content = f'\[{tile_pack}] • {size}x{size} • {solved}/{total} ({percent:.1f}%)'
