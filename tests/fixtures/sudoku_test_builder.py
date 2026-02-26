from typing import Self

import numpy as np

from pydoku.domain.models.sudoku import Sudoku, SudokuBuilder
from pydoku.domain.models.types import Array9, Array9x9


class SudokuTestBuilder:
    def __init__(self) -> None:
        self._initial_grid: Array9x9 = np.zeros((9, 9), dtype=int)

    def with_initial_grid(self, grid: Array9x9) -> Self:
        self._initial_grid = grid
        return self

    def with_initial_grid_value(self, row: int, colum: int, value: int) -> Self:
        self._initial_grid[row, colum] = value
        return self

    def with_initial_grid_row(self, row: int, values: Array9) -> Self:
        self._initial_grid[row] = values
        return self

    def with_initial_grid_column(self, column: int, values: Array9) -> Self:
        self._initial_grid[:, column] = values
        return self

    def build(self) -> Sudoku:
        return SudokuBuilder().with_initial_grid(self._initial_grid).build()
