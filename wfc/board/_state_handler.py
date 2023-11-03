def _state_handler(self, var, index, mode):
    from . import Board
    self: Board

    complete = self.complete.get()
    solved = self.solved.get()
    real_size = self.real_size.get()

    if solved == real_size:
        if not complete:
            self.complete.set(True)
    elif complete:
        self.complete.set(False)
