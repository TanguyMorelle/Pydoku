import numpy as np

from src.domain.models.sudoku import Sudoku
from src.domain.services.strategy import Strategy


class IntersectionRemoval(Strategy):
    def __init__(self, sudoku: Sudoku) -> None:
        super().__init__(sudoku)

    def execute(self) -> None:
        for _ in range(2):
            for y in range(3):
                for x in range(3):
                    self._single_line_intersection(y, x)
                    self._multi_line_intersection(y, x)
                    self._box_line_reduction(y, x)
            self.sudoku.transpose()

    def _single_line_intersection(self, y: int, x: int) -> None:
        u, v = 3 * y, 3 * x
        columns = list(set(range(9)) - set(range(v, v + 3)))
        block = self.sudoku.possible_values_grid[u: u + 3, v: v + 3, :]
        missing_values = self.sudoku.get_missing_values(self.sudoku.grid[u: u + 3, v: v + 3])
        for value in missing_values:
            y_pos, x_pos = np.where(block[:, :, value] == 1)
            if len(set(y_pos)) == 1 and len(y_pos) > 1:
                self.sudoku.possible_values_grid[u + y_pos[0], columns, value] = 0

    def _multi_line_intersection(self, y: int, x: int) -> None:
        u, v = 3 * y, 3 * x
        columns = list(set(range(9)) - set([v + i for i in range(3)]))
        sub_grid = self.sudoku.possible_values_grid[u:u + 3, columns, :]
        missing_values = self.sudoku.get_missing_values(self.sudoku.grid[u: u + 3, v: v + 3])
        for value in missing_values:
            lines_1, _ = np.where(sub_grid[:, :3, value] == 1)
            lines_2, _ = np.where(sub_grid[:, 3:, value] == 1)
            lines = set(list(lines_1) + list(lines_2))
            if len(lines) == 2 and len(lines_1) > 0 and len(lines_2) > 0:
                for i in lines:
                    self.sudoku.possible_values_grid[u + i, v: v + 3, value] = 0

    def _box_line_reduction(self, y: int, x: int) -> None:
        u, v = 3 * y, 3 * x
        columns = list(range(v, v + 3))
        missing_values = self.sudoku.get_missing_values(self.sudoku.grid[u:u + 3, v:v + 3])
        for value in missing_values:
            for i in range(3):
                for j in range(3):
                    x_pos, = np.where(self.sudoku.possible_values_grid[u + i, :, value] == 1)
                    if len(x_pos) and columns[0] <= min(x_pos) and max(x_pos) <= columns[-1]:
                        line_1, line_2 = list(set([u + k for k in range(3)]) - {u + i})
                        self.sudoku.possible_values_grid[line_1, columns, value] = 0
                        self.sudoku.possible_values_grid[line_2, columns, value] = 0
