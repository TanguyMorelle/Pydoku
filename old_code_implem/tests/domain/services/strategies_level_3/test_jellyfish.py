import numpy as np

from src.domain.models.cell import Cell
from src.domain.models.sudoku import Sudoku
from src.domain.services.strategies_level_3.jellyfish import Jellyfish


class TestJellyfish:
    def test_jellyfish(self) -> None:
        # Given
        value = 7
        sudoku = Sudoku(np.zeros((9, 9)))
        sudoku.possible_values_grid[:,:,:] = 0
        cells = [
            Cell(0, 0, (7,)), Cell(0, 1, (7,)), Cell(0, 2, (7,)), Cell(0, 3, (7,)), Cell(0, 4, (7,)), Cell(0, 5, (7,)), Cell(0, 6, (7,)), Cell(0, 7, (7,)), Cell(0, 8, (7,)),
            Cell(1, 0, (7,)), Cell(1, 1, (7,)), Cell(1, 3, (7,)), Cell(1, 7, (7,)),
            Cell(2, 0, (7,)), Cell(2, 1, (7,)), Cell(2, 2, (7,)), Cell(2, 3, (7,)), Cell(2, 7, (7,)),
            Cell(3, 0, (7,)), Cell(3, 3, (7,)), Cell(3, 7, (7,)),
            Cell(4, 0, (7,)), Cell(4, 1, (7,)), Cell(4, 2, (7,)), Cell(4, 3, (7,)), Cell(4, 4, (7,)), Cell(4, 5, (7,)), Cell(4, 6, (7,)), Cell(4, 7, (7,)), Cell(4, 8, (7,)),
            Cell(5, 0, (7,)), Cell(5, 3, (7,)), Cell(5, 7, (7,)),
            Cell(6, 0, (7,)), Cell(6, 1, (7,)), Cell(6, 3, (7,)),
            Cell(7, 0, (7,)), Cell(7, 1, (7,)), Cell(7, 3, (7,)), Cell(7, 4, (7,)), Cell(7, 7, (7,)), Cell(7, 8, (7,)),
            Cell(8, 0, (7,)), Cell(8, 1, (7,)), Cell(8, 2, (7,)), Cell(8, 3, (7,)), Cell(8, 4, (7,)), Cell(8, 5, (7,)), Cell(8, 6, (7,)), Cell(8, 8, (7,)),
        ]
        for cell in cells:
            i, j = cell.position
            sudoku.possible_values_grid[i, j, value] = 1

        jellyfish = Jellyfish(sudoku)

        # When
        jellyfish._jellyfish(value)

        # then
        updated_cells = [
            Cell(0, 0, (7,)), Cell(0, 1, (7,)), Cell(0, 3, (7,)), Cell(0, 7, (7,)),
            Cell(2, 0, (7,)), Cell(2, 1, (7,)), Cell(2, 3, (7,)), Cell(2, 7, (7,)),
            Cell(4, 0, (7,)), Cell(4, 1, (7,)), Cell(4, 3, (7,)), Cell(4, 7, (7,)),
            Cell(7, 0, (7,)), Cell(7, 1, (7,)), Cell(7, 3, (7,)), Cell(7, 7, (7,)),
            Cell(8, 0, (7,)), Cell(8, 1, (7,)), Cell(8, 3, (7,)),
        ]
        for cell in updated_cells:
            i, j = cell.position
            assert sudoku.possible_values_grid[i, j, value] == 0
        for cell in set(cells) - set(updated_cells):
            i, j = cell.position
            assert sudoku.possible_values_grid[i, j, value] == 1
