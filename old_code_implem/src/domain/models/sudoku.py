from math import floor

import numpy as np
from numpy import ndarray

from src.domain.models.cell import Cell
from src.domain.models.unit import Unit


class Sudoku:
    def __init__(self, initial_grid: ndarray) -> None:
        self.initial_grid = initial_grid
        self.grid = initial_grid
        self.possible_values_grid = np.ones((9, 9, 9))
        self.transposed = False
        self.initialisation()

    def initialisation(self) -> None:
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.possible_values_grid[i, j, :] = 0

    @classmethod
    def with_initial_values(cls, initial_values: list[tuple[int, int, int]]) -> "Sudoku":
        initial_grid = np.zeros((9, 9))
        for y, x, value in initial_values:
            initial_grid[y][x] = value
        return cls(initial_grid)

    def get_progress(self) -> int:
        y, _ = np.where(self.grid != 0)
        return floor(100 * len(y) / 81)

    def transpose(self) -> None:
        self.grid = self.grid.transpose((1, 0))
        self.possible_values_grid = self.possible_values_grid.transpose((1, 0, 2))
        self.transposed = not self.transposed

    def is_solved(self) -> bool:
        return self.grid.sum() == 9 * 45

    # set values
    def set_values(self):
        for i in range(9):
            for j in range(9):
                self.set_value_cell(i, j)
        for _ in range(2):
            for i in range(9):
                self.set_value_line(i)
            self.transpose()
        for y in range(3):
            for x in range(3):
                self.set_value_block(y, x)

    def set_value(self, i: int, j: int, value) -> None:
        self.grid[i][j] = value + 1
        self.possible_values_grid[i, j, :] = 0
        self.possible_values_grid[i, :, value] = 0
        self.possible_values_grid[:, j, value] = 0
        y, x = 3 * (i // 3), 3 * (j // 3)
        self.possible_values_grid[y:y + 3, x:x + 3, value] = 0

    def set_value_cell(self, i: int, j: int) -> None:
        values, = np.where(self.possible_values_grid[i, j] == 1)
        if len(values) == 1:
            self.set_value(i, j, values[0])

    def set_value_line(self, i: int) -> None:
        missing_values = self.get_missing_values(self.grid[i])
        for value in missing_values:
            columns, = np.where(self.possible_values_grid[i, :, value] == 1)
            if len(columns) == 1:
                self.set_value(i, columns[0], value)

    def set_value_block(self, y: int, x: int) -> None:
        u, v = y * 3, x * 3
        missing_values = self.get_missing_values(self.grid[u:u + 3, v:v + 3])
        for value in missing_values:
            y_pos, x_pos = np.where(self.possible_values_grid[u:u + 3, v:v + 3, value] == 1)
            cells = list(zip(y_pos, x_pos))
            if len(cells) == 1:
                i, j = u + cells[0][0], v + cells[0][1]
                self.set_value(i, j, value)

    @staticmethod
    def get_missing_values(arr: np.ndarray) -> list[int]:
        missing_elements = set(range(9))
        for i in arr.flatten():
            missing_elements -= {i - 1}
        return list(missing_elements)

    @staticmethod
    def get_n_valued_cells(arr: np.ndarray, n: int) -> list[Cell]:
        lines, columns = np.where(np.sum(arr, axis=2) == n)
        valid_cells = []
        for line, column in zip(lines, columns):
            values, = np.where(arr[line, column, :] == 1)
            valid_cells.append(Cell(line, column, tuple(values)))
        return valid_cells

    def get_n_optioned_unit(self, value: int, unit: Unit, n: int) -> list[tuple[Cell, Cell]]:
        if unit == Unit.LINE:
            return self._get_n_optioned_lines(value, n)
        if unit == Unit.COLUMN:
            return self._get_n_optioned_columns(value, n)
        if unit == Unit.BLOCK:
            return self._get_n_optioned_blocks(value, n)

    def _get_n_optioned_lines(self, value: int, n: int) -> list[tuple[Cell, Cell]]:
        cells = []
        for i in range(9):
            x_pos, = np.where(self.possible_values_grid[i, :, value] == 1)
            if len(x_pos) == n:
                cells.append((
                    Cell(i, x_pos[0], (value,)), Cell(i, x_pos[1], (value,))
                ))
        return cells

    def _get_n_optioned_columns(self, value: int, n: int) -> list[tuple[Cell, Cell]]:
        cells = []
        for j in range(9):
            y_pos, = np.where(self.possible_values_grid[:, j, value] == 1)
            if len(y_pos) == n:
                cells.append((
                    Cell(y_pos[0], j, (value,)), Cell(y_pos[1], j, (value,))
                ))
        return cells

    def _get_n_optioned_blocks(self, value: int, n: int) -> list[tuple[Cell, Cell]]:
        cells = []
        for y in range(3):
            for x in range(3):
                u, v = 3 * y, 3 * x
                y_pos, x_pos = np.where(self.possible_values_grid[u:u + 3, v:v + 3, value] == 1)
                if len(y_pos) == n:
                    cells.append((
                        Cell(u + y_pos[0], v + x_pos[0], (value,)), Cell(u + y_pos[1], v + x_pos[1], (value,))
                    ))
        return cells

    def get_possible_cells_for_value(self, value: int) -> list[Cell]:
        y_pos, x_pos = np.where(self.possible_values_grid[:, :, value] == 1)
        return [Cell(i, j, (value,)) for i, j in zip(y_pos, x_pos)]
