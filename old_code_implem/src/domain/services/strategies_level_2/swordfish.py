import numpy as np

from src.domain.models.sudoku import Sudoku
from src.domain.services.strategy import Strategy

Triplet = list[list[int, int, int], list[int, int, int]]


class Swordfish(Strategy):
    def __init__(self, sudoku: Sudoku):
        super().__init__(sudoku)

    def execute(self) -> None:
        for _ in range(2):
            for value in range(9):
                self._swordfish(value)
            self.sudoku.transpose()

    def _swordfish(self, value: int) -> None:
        valid_lines = self._get_valid_lines(value)
        triplets = self._get_triplets(valid_lines, value)
        for lines, columns in triplets:
            i, j, k = lines
            cells = [(m, n) for m in range(9) for n in columns]
            valid_cells = [(m, n) for m in [i, j, k] for n in columns]
            cells = set(cells) - set(valid_cells)
            for cell in cells:
                self.sudoku.possible_values_grid[cell[0], cell[1], value] = 0

    def _get_valid_lines(self, value: int) -> list[int]:
        value_on_lines = np.sum(self.sudoku.possible_values_grid[:, :, value], axis=1)
        valid_lines_2, = np.where(value_on_lines == 2)
        valid_lines_3, = np.where(value_on_lines == 3)
        valid_lines = list(valid_lines_2) + list(valid_lines_3)
        return valid_lines

    def _get_triplets(self, valid_lines: list[int], value: int) -> list[Triplet]:
        triplets = []
        for i in range(len(valid_lines)):
            for j in range(i + 1, len(valid_lines)):
                for k in range(j + 1, len(valid_lines)):
                    lines = [valid_lines[i], valid_lines[j], valid_lines[k]]
                    _, columns = np.where(self.sudoku.possible_values_grid[lines, :, value] == 1)
                    if len(set(columns)) == 3:
                        triplets.append([lines, list(set(columns))])
        return triplets
