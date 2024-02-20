import numpy as np
import pytest

from src.adapters.exceptions import InvalidInputException
from src.adapters.sudoku_csv_handler import SudokuCsvHandler
from tests.fixtures.grids.arrays import EASY_GRID
from tests.LoaderSUT import LoaderSUT


class SudokuCsvHandlerUTest(LoaderSUT):
    def test__load_should_raise_exception_if_file_not_csv(self) -> None:
        # Given
        handler = SudokuCsvHandler()

        # When
        with pytest.raises(InvalidInputException):
            handler.load("some_file.txt")

    def test__load_should_raise_exception_if_invalid_grid_shape(self) -> None:
        # Given
        handler = SudokuCsvHandler()
        path = self.get_grid("invalid_grid_shape.csv")

        # When
        with pytest.raises(InvalidInputException):
            handler.load(path)

    def test__load_should_raise_exception_if_invalid_grid_type(self) -> None:
        # Given
        handler = SudokuCsvHandler()
        path = self.get_grid("invalid_grid_type.csv")

        # When
        with pytest.raises(InvalidInputException):
            handler.load(path)

    def test__load_should_raise_exception_if_invalid_grid_value_negative(self) -> None:
        # Given
        handler = SudokuCsvHandler()
        path = self.get_grid("invalid_grid_value_2.csv")

        # When
        with pytest.raises(InvalidInputException):
            handler.load(path)

    def test__load_should_raise_exception_if_invalid_grid_value_over_9(self) -> None:
        # Given
        handler = SudokuCsvHandler()
        path = self.get_grid("invalid_grid_value_1.csv")

        # When
        with pytest.raises(InvalidInputException):
            handler.load(path)

    def test__load_should_return_sudoku(self) -> None:
        # Given
        handler = SudokuCsvHandler()
        path = self.get_grid("easy_grid.csv")

        # When
        sudoku = handler.load(path)

        # Then
        assert np.array_equal(sudoku.initial_grid, EASY_GRID)

    def test__save_should_write_grid_to_file(self, tmp_path) -> None:
        name = "test_csv_handler_save"
        filename = tmp_path / name
        full_filename = tmp_path / (name + "_grid.csv")
        grid_path = self.get_grid("easy_grid.csv")
        handler = SudokuCsvHandler()
        sudoku = handler.load(grid_path)

        handler.save(sudoku, filename)

        assert np.array_equal(np.genfromtxt(full_filename, delimiter=","), EASY_GRID)
