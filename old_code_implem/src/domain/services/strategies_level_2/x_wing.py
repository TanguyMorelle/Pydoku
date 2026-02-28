import numpy as np

from src.domain.models.sudoku import Sudoku
from src.domain.services.strategy import Strategy


class XWing(Strategy):
    def __init__(self, sudoku: Sudoku) -> None:
        super().__init__(sudoku)

    def execute(self) -> None:
        for _ in range(2):
            for value in range(9):
                self._x_wing(value)
            self.sudoku.transpose()

    def _x_wing(self, value: int) -> None:
        valid_lines = self._get_valid_lines(value)
        x_wing_couples = self._get_couples(valid_lines)
        for line_1, line_2, column_1, column_2 in x_wing_couples:
            lines_to_update = list(set(range(9)) - {line_1, line_2})
            self.sudoku.possible_values_grid[lines_to_update, column_1, value] = 0
            self.sudoku.possible_values_grid[lines_to_update, column_2, value] = 0

    def _get_valid_lines(self, value: int) -> dict[int, list[int, int]]:
        valid_lines = {}
        for line in range(9):
            columns, = np.where(self.sudoku.possible_values_grid[line, :, value] == 1)
            if len(columns) == 2:
                valid_lines[line] = list(columns)
        return valid_lines

    @staticmethod
    def _get_couples(valid_lines: dict[int, list[int, int]]) -> list[list[int, int, int, int]]:
        couples = []
        lines = list(valid_lines.keys())
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                if np.array_equal(valid_lines[lines[i]], valid_lines[lines[j]]):
                    column_1, column_2 = valid_lines[lines[i]]
                    couples.append([lines[i], lines[j], column_1, column_2])
        return couples
