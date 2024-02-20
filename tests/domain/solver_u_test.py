from unittest.mock import mock_open, patch

from src.adapters.sudoku_seq_handler import SudokuSeqHandler
from src.domain.solver import Solver
from tests.fixtures.grids.sequences import FILLED_GRID_SEQUENCE


class SolverUTest:
    def test__solve_blocked(self):
        # Given
        sudoku = SudokuSeqHandler().load("." * 81)
        solver = Solver(sudoku)

        # When
        with patch("numpy.savetxt"):
            with patch("builtins.open", mock_open()):
                result = solver.solve()

        # Then
        assert result is False

    def test__solve_valid_grid(self):
        # Given
        sudoku = SudokuSeqHandler().load(FILLED_GRID_SEQUENCE)
        solver = Solver(sudoku)

        # When
        with patch("numpy.savetxt"):
            with patch("builtins.open", mock_open()):
                result = solver.solve()

        # Then
        assert result is True
