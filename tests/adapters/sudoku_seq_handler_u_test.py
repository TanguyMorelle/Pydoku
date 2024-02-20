import numpy as np
import pytest

from src.adapters.exceptions import InvalidInputException
from src.adapters.sudoku_seq_handler import SudokuSeqHandler
from tests.fixtures.grids.arrays import EASY_GRID
from tests.fixtures.grids.sequences import (
    EASY_GRID_SEQUENCE,
    EASY_GRID_SEQUENCE_WITH_RANDOM_CHARS,
)


class SeqSudokuLoaderUTest:
    def test__load_invalid_sequence_should_raise_exception(self) -> None:
        # Given
        invalid_sequence = "12345"
        handler = SudokuSeqHandler()

        # When
        with pytest.raises(InvalidInputException):
            handler.load(invalid_sequence)

    def test__load_with_valid_sequence_should_return_sudoku(self) -> None:
        # Given
        sequence = EASY_GRID_SEQUENCE_WITH_RANDOM_CHARS
        handler = SudokuSeqHandler()

        # When
        sudoku = handler.load(sequence)

        # Then
        assert np.array_equal(sudoku.initial_grid, EASY_GRID)

    def test__save_should_write_sequence_to_file(self, tmp_path) -> None:
        # Given
        name = "test_seq_sudoku_loader_save"
        filename = tmp_path / name
        save_filename = tmp_path / (name + "_seq.txt")
        handler = SudokuSeqHandler()
        sudoku = handler.load(EASY_GRID_SEQUENCE_WITH_RANDOM_CHARS)

        # When
        handler.save(sudoku, filename)

        # Then
        assert save_filename.read_text() == EASY_GRID_SEQUENCE
