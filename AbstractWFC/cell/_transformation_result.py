from dataclasses import dataclass

from AbstractWFC.cell import State


@dataclass
class TransformationResult:
    cell: 'AbcCell'
    tiles_changed: bool
    curr_state: State
    prev_state: State


from AbstractWFC.cell.abc_cell import AbcCell
