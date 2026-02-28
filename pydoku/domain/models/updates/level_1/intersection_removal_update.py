from collections.abc import Sequence
from enum import Enum
from typing import Self

from pydantic import BaseModel

from pydoku.domain.models.cell import Cell
from pydoku.domain.models.updates.update import OptionsUpdate


class IntersectionRemovalTypes(Enum):
    BOX_LINE_REDUCTION = "BOX_LINE_REDUCTION"
    SINGLE_LINE_POINTING_SETS = "SINGLE_LINE_POINTING_SETS"
    MULTI_LINE_POINTING_SETS = "MULTI_LINE_POINTING_SETS"


class IntersectionRemovalUpdate(BaseModel, OptionsUpdate):
    cells: list[Cell]
    values: Sequence[int]
    options_updates: list[Cell]
    type: IntersectionRemovalTypes
    transposed: bool

    def transpose(self) -> Self:
        self.cells = sorted(cell.transpose() for cell in self.cells)
        self.options_updates = sorted(cell.transpose() for cell in self.options_updates)
        self.transposed = not self.transposed
        return self

    def realign(self) -> Self:
        if self.transposed:
            self.transpose()
        return self

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IntersectionRemovalUpdate):
            return False
        return (
            sorted(self.cells) == sorted(other.cells)
            and sorted(self.values) == sorted(other.values)
            and sorted(self.options_updates) == sorted(other.options_updates)
            and self.type == other.type
            and self.transposed == other.transposed
        )
