from unittest.mock import Mock

import numpy as np

from src.domain.models.sudoku import Sudoku
from src.domain.services.strategies_level_2.single_chains import SingleChains


class TestSingleChains:
    def test_should_return_cycles(self) -> None:
        # Given
        sudoku = Sudoku(np.zeros((9, 9)))
        sudoku.possible_values_grid = np.zeros((9, 9, 9))
        positions = [
            (0, 0), (0, 1), (0, 3), (1, 0), (1, 4),
            (3, 2), (3, 5), (4, 0), (4, 2), (4, 6), (4, 8), (5, 3), (5, 6),
            (6, 2), (6, 6), (7, 4), (7, 5), (8, 1), (8, 8)
        ]
        for i, j in positions:
            sudoku.possible_values_grid[i, j, 4] = 1

        single_chains = SingleChains(sudoku)

        # When
        chains = single_chains._get_cycles(4)

        # Then
        assert len(chains) == 2

    def test_should_execute_rule_2(self) -> None:
        # Given
        sudoku = Sudoku(np.zeros((9, 9)))
        sudoku.possible_values_grid = np.zeros((9, 9, 9))
        positions = [
            (0, 0), (0, 1), (0, 3), (1, 0), (1, 4),
            (3, 2), (3, 5), (4, 0), (4, 6), (4, 8), (5, 3), (5, 6),
            (6, 2), (6, 6), (7, 4), (7, 5), (8, 1), (8, 8)
        ]
        for i, j in positions:
            sudoku.possible_values_grid[i, j, 4] = 1

        single_chains = SingleChains(sudoku)

        # When
        single_chains._single_chains(4, rule_4=False)

        # Then
        invalid_positions = [
            (0, 1), (0, 3), (1, 0), (3, 5), (4, 0), (5, 6), (6, 2), (7, 4), (8, 8)
        ]
        for i, j in invalid_positions:
            assert single_chains.sudoku.possible_values_grid[i, j, 4] == 0
        for i, j in set(positions) - set(invalid_positions):
            assert single_chains.sudoku.possible_values_grid[i, j, 4] == 1

    def test_should_execute_rule_4(self) -> None:
        # Given
        sudoku = Sudoku(np.zeros((9, 9)))
        sudoku.possible_values_grid = np.zeros((9, 9, 9))
        positions = [
            (0, 0), (0, 1), (0, 3), (1, 0), (1, 4),
            (3, 2), (3, 5), (4, 0), (4, 2), (4, 6), (4, 8), (5, 3), (5, 6),
            (6, 2), (6, 6), (7, 4), (7, 5), (8, 1), (8, 8)
        ]
        for i, j in positions:
            sudoku.possible_values_grid[i, j, 4] = 1

        single_chains = SingleChains(sudoku)

        # When
        single_chains._single_chains(4, rule_2=False)

        # Then
        assert single_chains.sudoku.possible_values_grid[4, 2, 4] == 0
        assert single_chains.sudoku.possible_values_grid[4, 0, 4] == 0
        for i, j in set(positions) - {(4, 0), (4, 2)}:
            assert single_chains.sudoku.possible_values_grid[i, j, 4] == 1
