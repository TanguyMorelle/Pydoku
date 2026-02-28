from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Self

import numpy as np

from pydoku.domain.models.grid import PossibleValuesGrid, ValuesGrid
from pydoku.domain.models.types import Array9x9, Array9x9x9
from pydoku.domain.models.updates.update import Update
from pydoku.utils.grid_tools import get_visibility


@dataclass
class Sudoku:
    initial_grid: ValuesGrid
    grid: ValuesGrid
    options: PossibleValuesGrid
    transposed: bool
    updates: dict[int, list[Update]]

    @contextmanager
    def transpose(self) -> Generator[Sudoku, ..., ...]:
        self._transpose()
        try:
            yield self
        finally:
            self._transpose()

    def _transpose(self) -> None:
        self.initial_grid = self.initial_grid.transpose((1, 0))
        self.grid = self.grid.transpose((1, 0))
        self.options = self.options.transpose((1, 0, 2))
        self.transposed = not self.transposed

    def realign(self) -> None:
        if self.transposed:
            self._transpose()

    @property
    def progress(self) -> int:
        return int(100 * np.count_nonzero(self.grid) / 81)

    @property
    def solved(self) -> bool:
        return self.grid.sum() == 9 * 45

    def add_update(self, step: int, update: Update) -> None:
        updates = self.updates.get(step, [])
        updates.append(update)
        self.updates[step] = updates


class SudokuBuilder:
    def __init__(self) -> None:
        self._initial_grid = ValuesGrid(
            np.zeros(
                (
                    9,
                    9,
                ),
                dtype=int,
            )
        )
        self._grid = None
        self._options = None
        self._transposed = False

    def with_initial_grid(self, grid: Array9x9) -> Self:
        self._initial_grid = ValuesGrid(grid)
        return self

    def with_grid(self, grid: Array9x9) -> Self:
        self._grid = ValuesGrid(grid)
        return self

    def with_options(self, options: Array9x9x9) -> Self:
        self._options = PossibleValuesGrid(options)
        return self

    def transposed(self) -> Self:
        self._transposed = True
        return self

    def _get_grid(self) -> ValuesGrid:
        if self._grid is None:
            return self._initial_grid.copy()
        return self._grid

    def _get_options(self) -> PossibleValuesGrid:
        if self._options is None:
            options = PossibleValuesGrid(np.ones((9, 9, 9), dtype=int))
            grid = self._get_grid()
            for row in range(9):
                for column in range(9):
                    if (value := grid[row, column]) != 0:
                        options[row, column] = np.zeros((9,), dtype=int)
                        visibility = get_visibility((row, column))
                        for position in visibility:
                            options[*position, value - 1] = 0
            return options
        return self._options

    def build(self) -> Sudoku:
        return Sudoku(
            initial_grid=self._initial_grid,
            grid=self._get_grid(),
            options=self._get_options(),
            transposed=self._transposed,
            updates={},
        )
