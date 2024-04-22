from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from src.domain.cell import Cell
from src.domain.strategies.strategy_object import StrategyObject
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

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, GridUpdate):
            return False
        return self.__dict__ == other.__dict__

    def __str__(self) -> str:
        match self.unit:
            case Units.ROW:
                msg = f" [r{self.cell.row + 1}]"
            case Units.COLUMN:
                msg = f" [c{self.cell.column + 1}]"
            case Units.BLOCK:
                msg = f" [b{self.cell.block + 1}]"
            case _:
                msg = ""
        repr_ = f"[SET] unique option {self.cell.values[0] + 1}{msg} @ r{self.cell.row + 1}c{self.cell.column + 1}\n"
        if len(self.possible_values_updates):
            for cell in self.possible_values_updates:
                repr_ += f"    | removes {cell.values[0] + 1} @ r{cell.row + 1}c{cell.column + 1}\n"
        return repr_


@dataclass
class ObjUpdate(Update):
    obj: "StrategyObject"
    transposed: bool
    possible_values_updates: list[Cell]

    def realign(self) -> "ObjUpdate":
        if self.transposed:
            return ObjUpdate(
                obj=self.obj.realign(),
                transposed=False,
                possible_values_updates=[
                    cell.transpose() for cell in self.possible_values_updates
                ],
            )
        return self

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ObjUpdate):
            return self.__dict__ == other.__dict__
        return False

    def __str__(self) -> str:
        repr_ = str(self.obj)
        if len(self.possible_values_updates):
            for cell in self.possible_values_updates:
                values = ", ".join(str(value + 1) for value in cell.values)
                repr_ += f"    | removes r{cell.row + 1}c{cell.column + 1}[{values}]\n"
        return repr_
