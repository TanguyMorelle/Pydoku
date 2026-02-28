from typing import Optional

import numpy as np

from src.domain.models.sudoku import Sudoku
from src.domain.services.strategy import Strategy

Position = tuple[int, int]


class AvoidableRectangles(Strategy):
    def __init__(self, sudoku: Sudoku) -> None:
        super().__init__(sudoku)

    def execute(self) -> None:
        for _ in range(2):
            filled_grid = self.sudoku.grid - self.sudoku.initial_grid
            for y in range(3):
                for x in range(3):  # {1, 2} should be enough
                    self._avoidable_rectangles(y, x, filled_grid)
            self.sudoku.transpose()

    def _avoidable_rectangles(self, y: int, x: int, filled_grid: np.ndarray[(9, 9)]) -> None:
        other_block_column = set(range(3)) - {x}
        for value in range(1, 10):
            pos = self._get_cell_with_value(y, x, value, filled_grid)
            if pos:
                for block in other_block_column:
                    block_pos = self._get_cell_with_value(y, block, value, filled_grid)
                    if block_pos:
                        self._check_for_rectangle(pos, block_pos, filled_grid)

    def _check_for_rectangle(self, pos_1: Position, pos_2: Position, grid: np.ndarray[(9, 9)]) -> None:
        value_1 = int(grid[pos_1[0], pos_2[1]])
        value_2 = int(grid[pos_2[0], pos_1[1]])
        if value_1 != 0 and self.sudoku.possible_values_grid[pos_2[0], pos_1[1], value_1] == 1:
            self.sudoku.remove_possible_values((pos_2[0], pos_1[1]), [value_1])
        if value_2 != 0 and self.sudoku.possible_values_grid[pos_1[0], pos_2[1], value_2] == 1:
            self.sudoku.remove_possible_values((pos_1[0], pos_2[1]), [value_2])

    @staticmethod
    def _get_cell_with_value(y: int, x: int, value: int, grid: np.ndarray[(9,9)]) -> Optional[Position]:
        u, v = y * 3, x * 3
        y_pos, x_pos = np.where(grid[u:u + 3, v:v + 3] == value)
        pos_: list[Position] = list(zip(y_pos, x_pos))
        if len(pos_) > 0:
            return pos_[0][0] + u, pos_[0][1] + v
        return

    def _get_filled_positions(self) -> list[Position]:
        y_filled, x_filled = np.where(self.sudoku.grid != 0)
        y_initial, x_initial = np.where(self.sudoku.initial_grid != 0)
        filled_positions = set(zip(y_filled, x_filled)) - set(zip(y_initial, x_initial))
        return list(filled_positions)
