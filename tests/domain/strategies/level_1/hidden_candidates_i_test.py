from src.adapters.sudoku_seq_handler import SudokuSeqHandler
from src.domain.solver import Solver
from tests.fixtures.grids.sequences import HIDDEN_CANDIDATES_GRID_SEQUENCE


class HiddenCandidatesITest:
    def test_should_use_hiddenCandidates_in_solver(self) -> None:
        # Given
        sudoku = SudokuSeqHandler().load(HIDDEN_CANDIDATES_GRID_SEQUENCE)
        solver = Solver(sudoku)

        # When
        is_solved = solver._solve()

        # Then
        assert is_solved
