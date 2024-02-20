from src.domain.data_loader import DataLoader
from src.domain.solver import Solver
from tests.fixtures.grids import EASY_GRID_SEQUENCE


class UnicityITest:
    def test_should_use_unicity_in_solver(self) -> None:
        # Given
        sudoku = DataLoader.from_sequence(EASY_GRID_SEQUENCE)
        solver = Solver(sudoku)

        # When
        is_solved = solver._solve()

        # Then
        assert is_solved
