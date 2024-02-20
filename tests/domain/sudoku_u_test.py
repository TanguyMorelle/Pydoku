from unittest.mock import Mock

import numpy as np
import pytest

from src.adapters.sudoku_seq_handler import SudokuSeqHandler
from src.domain.cell import Cell
from src.domain.sudoku import Sudoku
from src.domain.units import Units
from src.domain.updates import GridUpdate
from tests.fixtures.grids.arrays import (
    EASY_GRID,
    EASY_GRID_POSSIBLE_VALUES,
    EASY_GRID_SOLVED,
    EMPTY_GRID,
)


class SudokuUTest:
    def test__sudoku_should_setup_on_initialization(self) -> None:
        # Given
        sudoku = Sudoku(EASY_GRID, SudokuSeqHandler())

        # Then
        assert np.array_equal(sudoku.initial_grid, EASY_GRID)
        assert np.array_equal(sudoku.grid, EASY_GRID)
        assert np.array_equal(sudoku.possible_values_grid, EASY_GRID_POSSIBLE_VALUES)

    def test__sudoku_should_return_progress(self) -> None:
        # Given
        sudoku = Sudoku(EASY_GRID, SudokuSeqHandler())

        # Then
        assert sudoku.progress == 39

    def test__sudoku_solved_should_be_false_if_not_solved(self) -> None:
        # Given
        sudoku = Sudoku(EASY_GRID, SudokuSeqHandler())

        # Then
        assert not sudoku.solved

    def test__sudoku_solved_should_be_true_if_solved(self) -> None:
        # Given
        sudoku = Sudoku(EASY_GRID_SOLVED, SudokuSeqHandler())

        # Then
        assert sudoku.progress == 100
        assert sudoku.solved

    def test__sudoku_should_return_missing_values_in_row(self) -> None:
        # Given
        sudoku = Sudoku(EASY_GRID, SudokuSeqHandler())

        # Then
        assert sudoku.get_missing_values(Units.ROW, 1) == [0, 4, 5, 6, 8]

    def test__sudoku_should_return_missing_values_in_column(self) -> None:
        # Given
        sudoku = Sudoku(EASY_GRID, SudokuSeqHandler())

        # Then
        assert sudoku.get_missing_values(Units.COLUMN, 1) == [0, 2, 4, 5, 7, 8]

    def test__sudoku_should_return_missing_values_in_block(self) -> None:
        # Given
        sudoku = Sudoku(EASY_GRID, SudokuSeqHandler())

        # Then
        assert sudoku.get_missing_values(Units.BLOCK, 4) == [1, 3, 4, 5, 8]

    def test__sudoku_should_raise_error_if_invalid_unit(self) -> None:
        # Given
        sudoku = Sudoku(EASY_GRID, SudokuSeqHandler())

        # Then
        with pytest.raises(ValueError):
            sudoku.get_missing_values(Units.CELL, 4)

    def test__sudoku_should_transpose_grid(self) -> None:
        # Given
        sudoku = Sudoku(EASY_GRID, SudokuSeqHandler())

        # When
        sudoku.transpose()

        # Then
        assert np.array_equal(sudoku.grid, EASY_GRID.transpose(1, 0))
        assert np.array_equal(sudoku.initial_grid, EASY_GRID.transpose(1, 0))
        assert np.array_equal(
            sudoku.possible_values_grid, EASY_GRID_POSSIBLE_VALUES.transpose(1, 0, 2)
        )

    def test__sudoku_should_realign_if_transposed(self) -> None:
        # Given
        sudoku = Sudoku(EASY_GRID, SudokuSeqHandler())
        sudoku.transpose()

        # When
        sudoku.realign()

        # Then
        assert not sudoku.transposed
        assert np.array_equal(sudoku.grid, EASY_GRID)
        assert np.array_equal(sudoku.initial_grid, EASY_GRID)
        assert np.array_equal(sudoku.possible_values_grid, EASY_GRID_POSSIBLE_VALUES)

    def test__sudoku_should_not_realign_if_not_transposed(self) -> None:
        # Given
        sudoku = Sudoku(EASY_GRID, SudokuSeqHandler())

        # When
        sudoku.realign()

        # Then
        assert not sudoku.transposed
        assert np.array_equal(sudoku.grid, EASY_GRID)
        assert np.array_equal(sudoku.initial_grid, EASY_GRID)
        assert np.array_equal(sudoku.possible_values_grid, EASY_GRID_POSSIBLE_VALUES)

    def test__sudoku_should_update_grid(self) -> None:
        # Given
        sudoku = Sudoku(EMPTY_GRID, SudokuSeqHandler())

        # When
        sudoku.update(
            [
                GridUpdate(
                    unit=Units.ROW,
                    transposed=False,
                    cell=Cell(0, 1, (1,)),
                    possible_values_updates=[Cell(1, 1, (1,))],
                ),
                GridUpdate(
                    unit=Units.ROW,
                    transposed=True,
                    cell=Cell(5, 5, (2,)),
                    possible_values_updates=[
                        Cell(4, 3, (2,)),
                        Cell(4, 4, (2,)),
                    ],
                ),
            ]
        )

        # Then
        assert sudoku.grid[0, 1] == 2
        assert sudoku.grid[5, 5] == 3
        assert np.array_equal(
            sudoku.possible_values_grid[0, 1, :], np.zeros(9, dtype=int)
        )
        assert np.array_equal(
            sudoku.possible_values_grid[5, 5, :], np.zeros(9, dtype=int)
        )
        assert np.array_equal(
            sudoku.possible_values_grid[1, 1, :], np.array([1, 0, 1, 1, 1, 1, 1, 1, 1])
        )
        assert np.array_equal(
            sudoku.possible_values_grid[3, 4, :], np.array([1, 1, 0, 1, 1, 1, 1, 1, 1])
        )
        assert np.array_equal(
            sudoku.possible_values_grid[4, 4, :], np.array([1, 1, 0, 1, 1, 1, 1, 1, 1])
        )
        updated_positions = {(0, 1), (5, 5), (1, 1), (3, 4), (4, 4)}
        positions = (
            set((row, column) for row in range(9) for column in range(9))
            - updated_positions
        )
        for position in positions:
            assert np.array_equal(
                sudoku.possible_values_grid[position], np.ones(9, dtype=int)
            )
            assert sudoku.grid[position] == 0

    def test__sudoku_should_raise_error_if_sudoku_is_transposed(self) -> None:
        # Given
        sudoku = Sudoku(EASY_GRID, SudokuSeqHandler())
        sudoku.transpose()

        # When
        with pytest.raises(ValueError):
            sudoku.update(
                [
                    GridUpdate(
                        unit=Units.ROW,
                        transposed=True,
                        cell=Cell(0, 1, (1,)),
                        possible_values_updates=[Cell(1, 1, (1,))],
                    )
                ]
            )

    def test__save_should_save_sudoku(self, tmp_path) -> None:
        # Given
        seq_sudoku_loader_mock = Mock(SudokuSeqHandler)
        sudoku = Sudoku(EASY_GRID, seq_sudoku_loader_mock)

        # When
        sudoku.save("some_name")

        # Then
        assert seq_sudoku_loader_mock.save.called_once_with(sudoku, "some_name")
