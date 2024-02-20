from src.adapters.sudoku_seq_handler import SudokuSeqHandler
from src.domain.solver import Solver
from tests.fixtures.grids.sequences import EASY_GRID_SEQUENCE


class UnicityITest:
    def test_should_use_unicity_in_solver(self) -> None:
        # Given
        sudoku = SudokuSeqHandler().load(EASY_GRID_SEQUENCE)
        solver = Solver(sudoku)

        # When
        is_solved = solver._solve()

        # Then
        assert is_solved
