from copy import deepcopy

import numpy as np

from src.domain.grid import PossibleValuesGrid, ValuesGrid
from src.domain.units import Units
from src.utils.updates import GridUpdate, PossibleValuesUpdate


class Sudoku:
    def __init__(self, initial_grid: np.ndarray) -> None:
        self.initial_grid = ValuesGrid(deepcopy(initial_grid))
        self.grid = ValuesGrid(initial_grid)
        self.possible_values_grid = PossibleValuesGrid(np.ones((9, 9, 9)))
        self.transposed = False
        self._setup()

    def _setup(self) -> None:
        for row in range(9):
            for column in range(9):
                if self.grid[row][column] != 0:
                    self.possible_values_grid[row, column, :] = 0

    @property
    def progress(self) -> int:
        y, _ = np.where(self.grid != 0)
        return int(100 * len(y) / 81)

    @property
    def solved(self) -> bool:
        return self.grid.sum() == 9 * 45

    def get_missing_values(self, unit: Units, n: int) -> list[int]:
        match unit:
            case Units.ROW:
                arr = self.grid.get_row(n)
            case Units.COLUMN:
                arr = self.grid.get_column(n)
            case Units.BLOCK:
                arr = self.grid.get_block(n)
            case _:
                raise ValueError("Invalid unit")
        missing_elements = set(range(9))
        for value in arr.flatten():
            missing_elements.discard(value - 1)
        return list(missing_elements)

    def transpose(self) -> None:
        self.grid = self.grid.transpose((1, 0))
        self.initial_grid = self.initial_grid.transpose((1, 0))
        self.possible_values_grid = self.possible_values_grid.transpose((1, 0, 2))
        self.transposed = not self.transposed

    def realign(self) -> None:
        if self.transposed:
            self.transpose()

    def update_grid(self, update: GridUpdate) -> None:
        if update.transposed != self.transposed:
            raise ValueError("Update and sudoku are not aligned")
        cell_to_update = update.cell
        value = cell_to_update.values[0]
        self.grid[*cell_to_update.position] = value + 1
        self.possible_values_grid[*cell_to_update.position, :] = 0
        for cell in update.possible_values_updates:
            self.possible_values_grid[*cell.position, value] = 0

    def update_possible_values_grid(self, update: PossibleValuesUpdate) -> None:
        if update.transposed != self.transposed:
            raise ValueError("Update and sudoku are not aligned")
        for cell in update.cells:
            self.possible_values_grid[*cell.position, list(cell.values)] = 0
