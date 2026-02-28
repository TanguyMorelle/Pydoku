from unittest.mock import Mock

import numpy as np

from src.domain.models.sudoku import Sudoku
from src.domain.services.strategies_level_2.remote_pairs import RemotePairs


class TestRemotePairs:
    def test_should_remove_values(self) -> None:
        # Given
        sudoku = Sudoku(np.zeros((9, 9)))
        sudoku.possible_values_grid = np.zeros((9, 9, 9))
        for i, j in [(0, 4), (0, 6), (2, 5), (2, 8), (3, 8)]:
            sudoku.possible_values_grid[i, j, [5, 8]] = 1
        for i, j in [(3, 4), (5, 5), (5, 6)]:
            sudoku.possible_values_grid[i, j, [7, 8]] = 1
        for i, j in [(6, 4), (6, 5)]:
            sudoku.possible_values_grid[i, j, [5, 7]] = 1
        sudoku.possible_values_grid[3, 6, [5, 7, 8]] = 1

        remote_pairs = RemotePairs(sudoku)

        # When
        remote_pairs()

        # Then
        for i, j in [(0, 4), (0, 6), (2, 5), (2, 8), (3, 8)]:
            values, = np.where(remote_pairs.sudoku.possible_values_grid[i, j, :] == 1)
            assert sorted(list(values)) == [5, 8]
        for i, j in [(5, 5), (5, 6)]:
            values, = np.where(remote_pairs.sudoku.possible_values_grid[i, j, :] == 1)
            assert sorted(list(values)) == [7, 8]
        for i, j in [(6, 4), (6, 5)]:
            values, = np.where(remote_pairs.sudoku.possible_values_grid[i, j, :] == 1)
            assert sorted(list(values)) == [5, 7]
        values, = np.where(remote_pairs.sudoku.possible_values_grid[3, 4, :] == 1)
        assert sorted(list(values)) == [7]
        values, = np.where(remote_pairs.sudoku.possible_values_grid[3, 6, :] == 1)
        assert sorted(list(values)) == [5, 7, 8]
