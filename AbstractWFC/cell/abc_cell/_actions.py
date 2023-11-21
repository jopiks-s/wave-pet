from AbstractWFC.cell import TransformationResult
from AbstractWFC.cell.abc_cell import AbcCell
from abc import ABC

class _Actions(AbcCell, ABC):
    def reset_cell(self):
        pass

    def apply_rules(self, rules: list[str]) -> TransformationResult:
        pass

    def collapse_cell(self, tile_name: str | None = None) -> TransformationResult:
        pass
