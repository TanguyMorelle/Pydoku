import numpy as np

from src.domain.strategies.strategy import Strategy
from src.domain.sudoku import Sudoku
from src.domain.units import Units
from src.domain.updates import Update


class IntersectionRemoval(Strategy):
    def __init__(self, sudoku: Sudoku) -> None:
        self.sudoku = sudoku
        self.updates: list[Update] = []

    def execute(self) -> list[Update]:
        for _ in range(2):
            for block in range(9):
                self._single_line_intersection(block)
                self._multi_line_intersection(block)
                self._box_line_reduction(block)
            self.sudoku.transpose()
        return self.updates

    def _single_line_intersection(self, block: int) -> None:
        u, v = divmod(block, 3)
        columns = list(set(range(9)) - set(range(v, v + 3)))
        missing_values = self.sudoku.get_missing_values(Units.BLOCK, block)
        for value in missing_values:
            y_pos, x_pos = np.where(self.sudoku.possible_values_grid.get_block(block, value) == 1)
            if len(set(y_pos)) == 1 and len(y_pos) > 1:
                self.sudoku.possible_values_grid[u + y_pos[0], columns, value] = 0

    def _multi_line_intersection(self, block: int) -> None:
        u, v = divmod(block, 3)
        columns = list(set(range(9)) - set([v + i for i in range(3)]))
        sub_grid = self.sudoku.possible_values_grid[u:u + 3, columns, :]
        missing_values = self.sudoku.get_missing_values(Units.BLOCK, block)
        for value in missing_values:
            lines_1, _ = np.where(sub_grid[:, :3, value] == 1)
            lines_2, _ = np.where(sub_grid[:, 3:, value] == 1)
            lines = set(list(lines_1) + list(lines_2))
            if len(lines) == 2 and len(lines_1) > 0 and len(lines_2) > 0:
                for i in lines:
                    self.sudoku.possible_values_grid[u + i, v: v + 3, value] = 0

    def _box_line_reduction(self, block: int) -> None:
        u, v = divmod(block, 3)
        columns = list(range(v, v + 3))
        missing_values = self.sudoku.get_missing_values(Units.BLOCK, block)
        for value in missing_values:
            for row in range(3):
                x_pos, = np.where(self.sudoku.possible_values_grid[u + row, :, value] == 1)
                if len(x_pos) and columns[0] <= min(x_pos) and max(x_pos) <= columns[-1]:
                    line_1, line_2 = list(set([u + k for k in range(3)]) - {u + row})
                    self.sudoku.possible_values_grid[line_1, columns, value] = 0
                    self.sudoku.possible_values_grid[line_2, columns, value] = 0
