from unittest.mock import Mock

import numpy as np

from src.domain.models.cell import Cell
from src.domain.models.sudoku import Sudoku
from src.domain.services.strategies_level_3.x_cycles import XCycles, XCycle


class TestXCycles:
    def test_should_return_cycles(self) -> None:
        # Given
        sudoku = Sudoku(np.zeros((9, 9)))
        sudoku.possible_values_grid = np.zeros((9, 9, 9))
        cells = [
            Cell(0, 5, (7,)), Cell(0, 8, (7,)),
            Cell(1, 2, (7,)), Cell(1, 3, (7,)), Cell(1, 5, (7,)), Cell(1, 8, (7,)),
            Cell(2, 1, (7,)), Cell(2, 2, (7,)), Cell(2, 6, (7,)), Cell(2, 8, (7,)),
            Cell(6, 1, (7,)), Cell(6, 2, (7,)), Cell(6, 3, (7,)), Cell(6, 8, (7,)),
            Cell(7, 2, (7,)), Cell(7, 8, (7,)),
            Cell(8, 3, (7,)), Cell(8, 5, (7,)), Cell(8, 6, (7,)),
        ]
        for cell in cells:
            sudoku.possible_values_grid[cell.line, cell.column, 7] = 1

        x_cycles = XCycles(sudoku)
        strong_link_cells, strong_links, strong_link_mapping, = x_cycles._get_cells_in_strong_links(7)
        cycle_mapping = x_cycles._get_visibility_mapping(strong_link_cells)

        # When
        cycles = x_cycles._get_cycles(strong_links, cycle_mapping, strong_link_mapping)

        # Then
        assert len(cycles) == 2
        assert cycles[0].sequence == [(2, 1), (6, 1), (7, 2), (7, 8), (8, 6), (2, 6)]
        assert cycles[1].sequence == [(2, 1), (2, 6), (8, 6), (7, 8), (7, 2), (6, 1)]

    def test_rule_1(self) -> None:
        # Given
        sudoku = Mock(Sudoku)
        sudoku.possible_values_grid = np.zeros((9, 9, 9))
        cells = [
            Cell(0, 5, (7,)), Cell(0, 8, (7,)),
            Cell(1, 2, (7,)), Cell(1, 3, (7,)), Cell(1, 5, (7,)), Cell(1, 8, (7,)),
            Cell(2, 1, (7,)), Cell(2, 2, (7,)), Cell(2, 6, (7,)), Cell(2, 8, (7,)),
            Cell(6, 1, (7,)), Cell(6, 2, (7,)), Cell(6, 3, (7,)), Cell(6, 8, (7,)),
            Cell(7, 2, (7,)), Cell(7, 8, (7,)),
            Cell(8, 3, (7,)), Cell(8, 5, (7,)), Cell(8, 6, (7,)),
        ]
        for cell in cells:
            sudoku.possible_values_grid[cell.line, cell.column, 7] = 1
        sudoku.get_possible_cells_for_value.return_value = cells

        cycle = XCycle([(2, 1), (6, 1), (7, 2), (7, 8), (8, 6), (2, 6)])

        x_cycles = XCycles(sudoku)

        # When
        x_cycles._rule_1(cycle, 7)

        # Then
        invalid_positions = [(2, 2), (2, 8), (6, 2), (6, 8)]
        for i, j in invalid_positions:
            assert x_cycles.sudoku.possible_values_grid[i, j, 7] == 0
        for i, j in set(list(map(lambda cell: cell.position, cells))) - set(invalid_positions):
            assert x_cycles.sudoku.possible_values_grid[i, j, 7] == 1

    def test_rule_2(self) -> None:
        # Given
        sudoku = Sudoku(np.zeros((9, 9)))
        sudoku.possible_values_grid = np.zeros((9, 9, 9))
        cells = [
            Cell(4, 2, (1,)), Cell(4, 7, (1,)),
            Cell(6, 2, (1,)),
            Cell(8, 0, (1,)), Cell(8, 7, (1,)),
        ]
        for cell in cells:
            sudoku.possible_values_grid[cell.line, cell.column, 1] = 1
        sudoku.possible_values_grid[8, 0, [2, 8]] = 1
        cycle = XCycle([(4, 2), (4, 7), (8, 7), (8, 0), (6, 2)])

        x_cycles = XCycles(sudoku)
        strong_link_cells, strong_links, strong_link_mapping, = x_cycles._get_cells_in_strong_links(1)

        # When
        x_cycles._rule_2(cycle, 1, strong_link_mapping)

        # Then
        for cell in cells:
            assert x_cycles.sudoku.possible_values_grid[cell.line, cell.column, 1] == 1
        assert x_cycles.sudoku.possible_values_grid[8, 0, 2] == 0
        assert x_cycles.sudoku.possible_values_grid[8, 0, 8] == 0
