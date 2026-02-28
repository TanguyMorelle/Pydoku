import itertools
import numpy as np

from src.domain.models.sudoku import Sudoku
from src.domain.services.strategy import Strategy

Position = tuple[int, int]


class HiddenCandidates(Strategy):
    def __init__(self, sudoku: Sudoku) -> None:
        super().__init__(sudoku)

    def execute(self) -> None:
        for _ in range(2):
            for i in range(9):
                self._line_subsets(i)
            self.sudoku.transpose()
        for y in range(3):
            for x in range(3):
                self._block_subsets(y, x)

    def _line_subsets(self, i: int) -> None:
        missing_values = self.sudoku.get_missing_values(self.sudoku.grid[i])
        for subsets in self._get_subsets(missing_values):
            for subset in subsets:
                _, columns = np.where(self.sudoku.possible_values_grid[i, :, subset] == 1)
                cells = [(i, j) for j in columns]
                self._update(cells, subset)

    def _block_subsets(self, y: int, x: int) -> None:
        u, v = 3 * y, 3 * x
        block = self.sudoku.possible_values_grid[u: u + 3, v: v + 3, :]
        missing_values = self.sudoku.get_missing_values(self.sudoku.grid[u: u + 3, v: v + 3])
        for subsets in self._get_subsets(missing_values):
            for subset in subsets:
                y_pos, x_pos, _ = np.where(block[:, :, subset] == 1)
                cells = [(u + i, v + j) for i, j in set(zip(y_pos, x_pos))]
                sudoku = self._update(cells, subset)

    def _update(self, cells: list[Position], subset: tuple[int]) -> None:
        if len(cells) == len(subset):
            joined_subset = list(set(range(9)) - set(subset))
            for i, j in cells:
                self.sudoku.possible_values_grid[i, j, joined_subset] = 0

    def _get_subsets(self, values: list[int]) -> list[list[tuple[int]]]:
        def get_combination(n: int) -> list[tuple[int]]:
            return list(itertools.combinations(values, n))

        return [get_combination(n) for n in range(2, len(values))]
