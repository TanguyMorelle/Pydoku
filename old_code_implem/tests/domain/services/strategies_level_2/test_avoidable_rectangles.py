from unittest.mock import Mock

import numpy as np

from src.domain.models.cell import Cell
from src.domain.models.sudoku import Sudoku
from src.domain.services.strategies_level_2.avoidable_rectangles import AvoidableRectangles


class TestAvoidableRectangles:
    def test_avoidable_rectangles(self) -> None:
        # Given
        initial_cells = [
            Cell(0, 0, (6,)),
            Cell(0, 3, (5,)),

            Cell(1, 2, (4,)),
            Cell(1, 6, (2,)),

            Cell(2, 0, (5,)),
            Cell(2, 2, (9,)),
            Cell(2, 4, (3,)),
            Cell(2, 8, (6,)),

            Cell(3, 3, (2,)),
            Cell(3, 7, (7,)),

            Cell(4, 1, (8,)),
            Cell(4, 4, (5,)),
            Cell(4, 7, (3,)),

            Cell(5, 1, (1,)),
            Cell(5, 5, (6,)),

            Cell(6, 0, (9,)),
            Cell(6, 4, (6,)),
            Cell(6, 6, (3,)),
            Cell(6, 8, (1,)),

            Cell(7, 2, (7,)),
            Cell(7, 6, (9,)),

            Cell(8, 5, (4,)),
            Cell(8, 8, (5,)),
        ]

        filled_cells = [
            Cell(0, 1, (2,)),
            Cell(0, 7, (9,)),
            Cell(0, 8, (3,)),

            Cell(1, 1, (3,)),
            Cell(1, 3, (6,)),
            Cell(1, 7, (5,)),
            Cell(1, 8, (7,)),

            Cell(2, 1, (7,)),
            Cell(2, 5, (2,)),
            Cell(2, 7, (1,)),

            Cell(3, 1, (9,)),
            Cell(3, 2, (5,)),
            Cell(3, 6, (6,)),

            Cell(4, 2, (6,)),
            Cell(4, 6, (1,)),

            Cell(5, 6, (5,)),

            Cell(7, 7, (6,)),

            Cell(8, 1, (6,)),
            Cell(8, 6, (7,)),
        ]

        possible_values = [
            Cell(0, 2, (0, 7)),
            Cell(0, 4, (0, 3, 6, 7)),
            Cell(0, 5, (0, 6, 7)),
            Cell(0, 6, (3, 8)),

            Cell(1, 0, (0, 7)),
            Cell(1, 4, (0, 7, 8)),
            Cell(1, 5, (0, 7, 8)),

            Cell(2, 3, (3, 7)),
            Cell(2, 6, (3, 7)),

            Cell(3, 0, (2, 3)),
            Cell(3, 4, (0, 3, 7,)),
            Cell(3, 5, (0, 2, 7)),
            Cell(3, 8, (3, 7)),

            Cell(4, 0, (1, 3, 6)),
            Cell(4, 3, (3, 6, 8)),
            Cell(4, 5, (6, 8)),
            Cell(4, 8, (1, 3, 8)),

            Cell(5, 0, (1, 2, 3, 6)),
            Cell(5, 2, (1, 2)),
            Cell(5, 3, (2, 3, 7, 8)),
            Cell(5, 4, (3, 6, 7, 8)),
            Cell(5, 7, (1, 3, 7)),
            Cell(5, 8, (1, 3, 7, 8)),

            Cell(6, 1, (3, 4)),
            Cell(6, 2, (1, 7)),
            Cell(6, 3, (6, 7)),
            Cell(6, 5, (4, 6, 7)),
            Cell(6, 7, (1, 3, 7)),

            Cell(7, 0, (0, 1, 2, 7)),
            Cell(7, 1, (3, 4)),
            Cell(7, 3, (0, 2, 7)),
            Cell(7, 4, (1, 7)),
            Cell(7, 5, (2, 4, 7)),
            Cell(7, 8, (1, 3, 7)),

            Cell(8, 0, (0, 1, 2, 7)),
            Cell(8, 2, (0, 1, 2, 7)),
            Cell(8, 3, (0, 2, 7, 8)),
            Cell(8, 4, (1, 7, 8)),
            Cell(8, 7, (1, 7)),
        ]

        initial_grid = np.zeros((9, 9))
        for cell in initial_cells:
            initial_grid[cell.line, cell.column] = cell.values[0]
        filled_grid = np.zeros((9, 9))
        for cell in filled_cells:
            filled_grid[cell.line, cell.column] = cell.values[0]
        possible_values_grid = np.zeros((9, 9, 9))
        for cell in possible_values:
            possible_values_grid[cell.line, cell.column, cell.values] = 1

        sudoku = Mock(Sudoku)
        sudoku.initial_grid = initial_grid
        sudoku.possible_values_grid = possible_values_grid
        sudoku.grid = initial_grid + filled_grid

        service = AvoidableRectangles(sudoku)
        assert sudoku.possible_values_grid[0, 5, 7] == 1

        # When
        service._avoidable_rectangles(0, 0, filled_grid)

        # Then
        sudoku.remove_possible_values.assert_called_once()
