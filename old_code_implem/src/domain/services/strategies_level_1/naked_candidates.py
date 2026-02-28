import itertools

import numpy as np

from src.domain.models.sudoku import Sudoku
from src.domain.services.strategy import Strategy

Position = tuple[int, int]


class NakedCandidates(Strategy):
    def __init__(self, sudoku: Sudoku) -> None:
        super().__init__(sudoku)

    def execute(self) -> None:
        for _ in range(2):
            for i in range(9):
                x_pos, = np.where(self.sudoku.grid[i, :] == 0)
                empty_cells = [(i, j) for j in x_pos]
                self._check_for_naked_groups(empty_cells)
            self.sudoku.transpose()

        for y in range(3):
            for x in range(3):
                u, v = 3 * y, 3 * x
                y_pos, x_pos = np.where(self.sudoku.grid[u:u + 3, v:v + 3] == 0)
                empty_cells = [(u + i, v + j) for i, j in zip(y_pos, x_pos)]
                self._check_for_naked_groups(empty_cells)

    def _check_for_naked_groups(self, cells: list[Position]) -> None:
        cell_combinations = self._get_subsets(cells)
        for cell_combination_size in cell_combinations:
            for combination in cell_combination_size:
                possible_values = []
                for position in combination:
                    values, = np.where(self.sudoku.possible_values_grid[position[0], position[1]] == 1)
                    possible_values += list(values)
                possible_values = list(set(possible_values))
                if len(combination) == len(possible_values):
                    invalid_cells = set(cells) - set(combination)
                    for position in invalid_cells:
                        self.sudoku.possible_values_grid[position[0], position[1], possible_values] = 0

    def _get_subsets(self, cells: list[Position]) -> list[list[tuple[Position]]]:
        def get_combination(n: int) -> list[tuple[Position]]:
            return list(itertools.combinations(cells, n))

        return [get_combination(n) for n in range(2, len(cells))]
