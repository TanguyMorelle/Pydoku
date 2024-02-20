from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from src.domain.cell import Cell
from src.domain.units import Units


class Update(ABC):
    @abstractmethod
    def realign(self) -> "Update": ...


@dataclass
class GridUpdate(Update):
    unit: Units
    transposed: bool
    cell: Cell
    possible_values_updates: list[Cell]

    def realign(self) -> "GridUpdate":
        if self.transposed:
            match self.unit:
                case Units.ROW:
                    unit = Units.COLUMN
                case Units.COLUMN:
                    unit = Units.ROW
                case _:
                    unit = self.unit
            cell = self.cell.transpose()
            possible_values_update = [
                cell.transpose() for cell in self.possible_values_updates
            ]
            return GridUpdate(
                unit=unit,
                transposed=False,
                cell=cell,
                possible_values_updates=possible_values_update,
            )
        return self

    def __repr__(self) -> str:
        match self.unit:
            case Units.ROW:
                msg = f" in {self.unit.value} {self.cell.row}"
            case Units.COLUMN:
                msg = f" in {self.unit.value} {self.cell.column}"
            case Units.BLOCK:
                msg = f" in {self.unit.value} {self.cell.block}"
            case _:
                msg = ""
        repr_ = f"[SET] unique option {self.cell.values[0] + 1} @ {self.cell.position}{msg}\n"
        if len(self.possible_values_updates):
            for cell in self.possible_values_updates:
                repr_ += f"    | removes {cell.values[0] + 1} @ {cell.position}\n"
        return repr_


@dataclass
class PossibleValuesUpdate(Update):
    transposed: bool
    obj: Any
    cells: list[Cell]

    def realign(self) -> "PossibleValuesUpdate":
        if self.transposed:
            cells = [cell.transpose() for cell in self.cells]
            return PossibleValuesUpdate(False, self.obj.realign(), cells)
        return self
