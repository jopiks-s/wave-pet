from abc import ABC

from AbstractWFC.board import AbcBoard
from AbstractWFC.cell import TransformationResult, State


class StatusHandler(AbcBoard, ABC):

    def reset_board(self):
        [cell.reset_cell() for row in self._board for cell in row]

        self.reset_status()

    def update_status(self, transfres: TransformationResult) -> TransformationResult:
        if not transfres.tiles_changed or transfres.curr_state == transfres.prev_state:
            return transfres

        if transfres.curr_state == State.Collapsed:
            self.stable_counter -= 1
            self.collapsed_counter += 1
        elif transfres.curr_state == State.Broken:
            self.stable_counter -= 1

            if transfres.prev_state == State.Collapsed:
                self.collapsed_counter -= 1

        if self.stable_counter == 0:
            self.complete = True

        return transfres

    def reset_status(self):
        self.stable_counter = self.cell_number
        self.collapsed_counter = 0
        self.complete = False
