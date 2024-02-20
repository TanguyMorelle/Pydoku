import numpy as np
import pytest

from src.utils.argument_parser import get_sudoku
from tests.fixtures.grids.arrays import EASY_GRID
from tests.fixtures.grids.sequences import EASY_GRID_SEQUENCE
from tests.LoaderSUT import LoaderSUT


class PydokuParserUTest(LoaderSUT):
    def test__get_sudoku_with_csv(self) -> None:
        # Given
        path = self.get_grid("easy_grid.csv")

        # When
        sudoku = get_sudoku(["--file", str(path)])

        # Then
        assert np.array_equal(sudoku.initial_grid, EASY_GRID)

    def test__get_sudoku_with_non_csv_file(self) -> None:
        # When
        with pytest.raises(SystemExit):
            get_sudoku(["--file", "easy_grid.txt"])

    def test__get_sudoku_with_seq(self) -> None:
        # When
        sudoku = get_sudoku(["--seq", EASY_GRID_SEQUENCE])

        # Then
        assert np.array_equal(sudoku.initial_grid, EASY_GRID)

    def test__get_sudoku_with_no_args(self) -> None:
        # When
        with pytest.raises(SystemExit):
            get_sudoku([])
