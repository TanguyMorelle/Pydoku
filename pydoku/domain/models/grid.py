import typing as t

import numpy as np

from pydoku.domain.models.types import (
    Array3x3,
    Array3x3x9,
    Array9,
    Array9x9,
    Array9x9x9,
    Grid,
)


class ValuesGrid[T: Array9x9](np.ndarray):
    def __new__(cls, initial_grid: Array9x9) -> ValuesGrid[Array9x9]:
        return t.cast(ValuesGrid[Array9x9], initial_grid.view(cls))

    def get_row(self, row: int) -> Subgrid[Array9]:
        return Subgrid(self[row, :])

    def get_column(self, column: int) -> Subgrid[Array9]:
        return Subgrid(self[:, column])

    def get_block(self, block: int) -> Subgrid[Array3x3]:
        u, v = divmod(block, 3)
        return Subgrid(self[3 * u : 3 * u + 3, 3 * v : 3 * v + 3])


class PossibleValuesGrid[T: Array9x9x9](np.ndarray):
    def __new__(cls, initial_grid: Array9x9x9) -> PossibleValuesGrid[Array9x9x9]:
        return t.cast(PossibleValuesGrid[Array9x9x9], initial_grid.view(cls))

    def get_cell(self, row: int, column: int) -> Array9:
        return self[row, column, :]

    def get_row(self, row: int) -> Array9x9:
        return self[row, :, :]

    def get_column(self, column: int) -> Array9x9:
        return self[:, column, :]

    def get_block(self, block: int) -> Array3x3x9:
        u, v = divmod(block, 3)
        return self[3 * u : 3 * u + 3, 3 * v : 3 * v + 3, :]

    def get_row_value(self, row: int, value: int) -> Array9:
        return self[row, :, value]

    def get_column_value(self, column: int, value: int) -> Array9:
        return self[:, column, value]

    def get_block_value(self, block: int, value: int) -> Array3x3:
        u, v = divmod(block, 3)
        return self[3 * u : 3 * u + 3, 3 * v : 3 * v + 3, value]


class Subgrid[T: Grid](np.ndarray):
    def __new__(cls, grid: T) -> Subgrid[T]:
        return t.cast(Subgrid[T], grid.view(cls))

    def get_missing_values(self) -> list[int]:
        return np.setdiff1d(np.arange(9), self.flatten() - 1).tolist()
