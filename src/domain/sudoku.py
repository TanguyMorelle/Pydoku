from copy import deepcopy
from typing import TYPE_CHECKING

import numpy as np

from src.domain.grid import PossibleValuesGrid, ValuesGrid
from src.domain.units import Units
from src.domain.updates import GridUpdate, Update
from src.utils.grid_tools import get_block

if TYPE_CHECKING:
    from src.domain.ports.sudoku_handler_interface import SudokuHandlerInterface


class Sudoku:
    def __init__(
        self, initial_grid: np.ndarray, sudoku_handler: "SudokuHandlerInterface"
    ) -> None:
        self.sudoku_handler = deepcopy(sudoku_handler)
        self.initial_grid = ValuesGrid(deepcopy(initial_grid))
        self.grid = deepcopy(self.initial_grid)
        self.possible_values_grid = PossibleValuesGrid(np.ones((9, 9, 9)))
        self.transposed = False
        self._setup()

    def _setup(self) -> None:
        for row in range(9):
            for column in range(9):
                if (value := self.grid[row][column]) != 0:
                    block = get_block((row, column))
                    self.possible_values_grid[row, column, :] = 0
                    self.possible_values_grid.get_row(row, value - 1)[:] = 0
                    self.possible_values_grid.get_column(column, value - 1)[:] = 0
                    self.possible_values_grid.get_block(block, value - 1)[:] = 0

    @property
    def progress(self) -> int:
        return int(100 * np.count_nonzero(self.grid) / 81)

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

    def update(self, updates: list[Update]) -> None:
        for update in list(map(lambda u: u.realign(), updates)):
            if isinstance(update, GridUpdate):
                self._update_grid(update)

    def _update_grid(self, update: GridUpdate) -> None:
        if self.transposed:
            raise ValueError("Update and sudoku are not aligned")
        cell_to_update = update.cell
        value = cell_to_update.values[0]
        self.grid[*cell_to_update.position] = value + 1
        self.possible_values_grid[*cell_to_update.position, :] = 0
        for cell in update.possible_values_updates:
            self.possible_values_grid[*cell.position, value] = 0

    def save(self, name: str) -> None:
        self.sudoku_handler.save(self, name)
