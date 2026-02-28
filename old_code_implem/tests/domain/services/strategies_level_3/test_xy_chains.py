import numpy as np

from src.domain.models.cell import Cell
from src.domain.models.sudoku import Sudoku
from src.domain.services.strategies_level_3.x_chain import XChains, XChain
from src.domain.services.strategies_level_3.xy_chains import XYChains


class TestXYChains:
    def test_get_chains_should_return_chains(self) -> None:
        pass

    def test_xy_chain(self) -> None:
        # Given
        sudoku = Sudoku(np.zeros((9, 9)))
        sudoku.possible_values_grid = np.zeros((9, 9, 9))
        cells = [
            Cell(1, 2, (3, 5)),
            Cell(4, 2, (3, 4)),
            Cell(4, 0, (2, 4)),
            Cell(7, 0, (2, 4)),
            Cell(6, 2, (4, 7)),
            Cell(8, 2, (7, 8)),
            Cell(8, 8, (7, 8)),
            Cell(2, 8, (1, 7)),
            Cell(2, 4, (1, 2)),
            Cell(3, 4, (2, 5)),
            Cell(4, 1, (5,)),
        ]
        for cell in cells:
            sudoku.possible_values_grid[cell.line, cell.column, cell.values] = 1

        xy_chains = XYChains(sudoku)

        # When
        xy_chains.execute()

        # Then
        assert xy_chains.sudoku.possible_values_grid[4, 1, 6] == 0
        for cell in set(cells) - {Cell(5, 7, (3,))}:
            for value in cell.values:
                assert xy_chains.sudoku.possible_values_grid[cell.line, cell.column, value] == 1
