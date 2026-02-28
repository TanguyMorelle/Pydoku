from typing import Self

from pydantic import BaseModel

from pydoku.domain.models.cell import Cell
from pydoku.domain.models.units import Units
from pydoku.domain.models.updates.update import GridUpdate


class UnicityUpdate(BaseModel, GridUpdate):
    unit: Units
    row: int
    column: int
    value: int
    options_updates: list[Cell]
    transposed: bool = False

    def transpose(self) -> Self:
        if self.unit == Units.ROW:
            self.unit = Units.COLUMN
        elif self.unit == Units.COLUMN:
            self.unit = Units.ROW
        self.row, self.column = self.column, self.row
        self.options_updates = [cell.transpose() for cell in self.options_updates]
        self.transposed = not self.transposed
        return self

    def realign(self) -> Self:
        if self.transposed:
            self.transpose()
        return self

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UnicityUpdate):
            return False
        return (
            self.unit == other.unit
            and self.row == other.row
            and self.column == other.column
            and self.value == other.value
            and self.transposed == other.transposed
            and sorted(self.options_updates) == sorted(self.options_updates)
        )
