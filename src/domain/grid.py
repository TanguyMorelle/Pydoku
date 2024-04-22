from abc import ABC, abstractmethod
from typing import Optional

import numpy.typing as npt


class Grid(npt.NDArray, ABC):
    @abstractmethod
    def get_row(self, row: int, value: Optional[int] = None) -> npt.NDArray: ...

    @abstractmethod
    def get_column(self, column: int, value: Optional[int] = None) -> npt.NDArray: ...

    @abstractmethod
    def get_block(self, block: int, value: Optional[int] = None) -> npt.NDArray: ...


class ValuesGrid(Grid):
    def __new__(cls, initial_grid: npt.NDArray) -> "ValuesGrid":
        return initial_grid.view(cls)

    def get_row(self, row: int, value: Optional[int] = None) -> npt.NDArray:
        return self[row, :]

    def get_column(self, column: int, value: Optional[int] = None) -> npt.NDArray:
        return self[:, column]

    def get_block(self, block: int, value: Optional[int] = None) -> npt.NDArray:
        u, v = divmod(block, 3)
        y, x = 3 * u, 3 * v
        return self[y : y + 3, x : x + 3]


class PossibleValuesGrid(Grid):
    def __new__(cls, initial_grid: npt.NDArray) -> "PossibleValuesGrid":
        return initial_grid.view(cls)

    def get_row(self, row: int, value: Optional[int] = None) -> npt.NDArray:
        if value is not None:
            return self[row, :, value]
        return self[row, :, :]

    def get_column(self, column: int, value: Optional[int] = None) -> npt.NDArray:
        if value is not None:
            return self[:, column, value]
        return self[:, column, :]

    def get_block(self, block: int, value: Optional[int] = None) -> npt.NDArray:
        u, v = divmod(block, 3)
        y, x = 3 * u, 3 * v
        if value is not None:
            return self[y : y + 3, x : x + 3, value]
        return self[y : y + 3, x : x + 3, :]
