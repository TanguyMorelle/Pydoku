from collections.abc import Sequence
from typing import Self

from pydantic import BaseModel

from pydoku.domain.models.cell import Cell
from pydoku.domain.models.updates.update import OptionsUpdate


class NakedCandidatesUpdate(BaseModel, OptionsUpdate):
    cells: list[Cell]
    values: Sequence[int]
    options_updates: list[Cell]
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
        if not isinstance(other, NakedCandidatesUpdate):
            return False
        return (
            sorted(self.cells) == sorted(other.cells)
            and sorted(self.values) == sorted(other.values)
            and sorted(self.options_updates) == sorted(other.options_updates)
            and self.transposed == other.transposed
        )
