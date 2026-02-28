import numpy as np

from src.domain.models.cell import Cell
from src.domain.models.sudoku import Sudoku
from src.domain.services.strategies_level_3.x_chain import XChains, XChain


class TestXCycles:
    def test_get_chains_should_return_chains(self) -> None:
        # Given
        sudoku = Sudoku(np.zeros((9, 9)))
        sudoku.possible_values_grid = np.zeros((9, 9, 9))
        cells = [
            Cell(3, 0, (3,)), Cell(3, 3, (3,)), Cell(3, 7, (3,)),
            Cell(4, 4, (3,)), Cell(4, 7, (3,)),
            Cell(5, 2, (3,)), Cell(5, 3, (3,)), Cell(5, 7, (3,)),
            Cell(6, 2, (3,)), Cell(6, 3, (3,)), Cell(6, 4, (3,)),
            Cell(7, 0, (3,)), Cell(7, 4, (3,)),
        ]
        for cell in cells:
            sudoku.possible_values_grid[cell.line, cell.column, 3] = 1

        x_chains = XChains(sudoku)

        # When
        cells, strong_links, strong_link_mapping = x_chains._get_cells_in_strong_links(3)
        cell_visibility_mapping = x_chains._get_cell_visibility_mapping(cells)
        chains = x_chains._get_chains(cell_visibility_mapping, strong_link_mapping)

        # Then
        assert chains == [
            XChain([(4, 7), (4, 4), (7, 4), (7, 0)]),
            XChain([(4, 7), (4, 4), (7, 4), (7, 0), (6, 2), (5, 2)]),
            XChain([(4, 7), (4, 4), (7, 4), (7, 0), (3, 0), (5, 2)]),
            XChain([(7, 0), (7, 4), (4, 4), (4, 7)]),
            XChain([(7, 0), (6, 2), (5, 2), (3, 0)]),
            XChain([(7, 0), (3, 0), (5, 2), (6, 2)]),
            XChain([(7, 4), (7, 0), (6, 2), (5, 2)]),
            XChain([(7, 4), (7, 0), (3, 0), (5, 2)]),
            XChain([(3, 0), (7, 0), (6, 2), (5, 2)]),
            XChain([(3, 0), (5, 2), (6, 2), (7, 0)]),
            XChain([(5, 2), (6, 2), (7, 0), (7, 4)]),
            XChain([(5, 2), (6, 2), (7, 0), (7, 4), (4, 4), (4, 7)]),
            XChain([(5, 2), (6, 2), (7, 0), (3, 0)]),
            XChain([(5, 2), (3, 0), (7, 0), (7, 4)]),
            XChain([(5, 2), (3, 0), (7, 0), (7, 4), (4, 4), (4, 7)]),
            XChain([(5, 2), (3, 0), (7, 0), (6, 2)]),
            XChain([(6, 2), (7, 0), (3, 0), (5, 2)]),
            XChain([(6, 2), (5, 2), (3, 0), (7, 0)]),
        ]

    def test_x_chain(self) -> None:
        # Given
        sudoku = Sudoku(np.zeros((9, 9)))
        sudoku.possible_values_grid = np.zeros((9, 9, 9))
        cells = [
            Cell(3, 0, (3,)), Cell(3, 3, (3,)), Cell(3, 7, (3,)),
            Cell(4, 4, (3,)), Cell(4, 7, (3,)),
            Cell(5, 2, (3,)), Cell(5, 3, (3,)), Cell(5, 7, (3,)),
            Cell(6, 2, (3,)), Cell(6, 3, (3,)), Cell(6, 4, (3,)),
            Cell(7, 0, (3,)), Cell(7, 4, (3,)),
        ]
        for cell in cells:
            sudoku.possible_values_grid[cell.line, cell.column, 3] = 1

        x_chains = XChains(sudoku)

        # When
        x_chains(3)

        # Then
        assert x_chains.sudoku.possible_values_grid[5, 7, 3] == 0
        for cell in set(cells) - {Cell(5, 7, (3,))}:
            assert x_chains.sudoku.possible_values_grid[cell.line, cell.column, 3] == 1

    def test_x_chain_bis(self) -> None:
        # Given
        sudoku = Sudoku(np.zeros((9, 9)))
        sudoku.possible_values_grid = np.zeros((9, 9, 9))
        cells = [
            Cell(0, 0, (1,)), Cell(0, 8, (1,)),
            Cell(2, 1, (1,)), Cell(2, 2, (1,)), Cell(2, 6, (1,)),
            Cell(5, 0, (1,)), Cell(5, 1, (1,)), Cell(5, 2, (1,)),
            Cell(6, 1, (1,)), Cell(6, 4, (1,)), Cell(6, 6, (1,)),
            Cell(7, 2, (1,)), Cell(7, 4, (1,)), Cell(7, 8, (1,)),
            Cell(8, 4, (1,)), Cell(8, 8, (1,)),
        ]
        for cell in cells:
            sudoku.possible_values_grid[cell.line, cell.column, 1] = 1

        x_chains = XChains(sudoku)

        # When
        x_chains(1)

        # Then
        assert x_chains.sudoku.possible_values_grid[2, 2, 1] == 0
        for cell in set(cells) - {Cell(2, 2, (1,))}:
            assert x_chains.sudoku.possible_values_grid[cell.line, cell.column, 1] == 1

    def test_x_chain_ter(self) -> None:
        # Given
        sudoku = Sudoku(np.zeros((9, 9)))
        sudoku.possible_values_grid = np.zeros((9, 9, 9))
        cells = [
            Cell(0, 0, (1,)), Cell(0, 2, (1,)), Cell(0, 6, (1,)), Cell(0, 7, (1,)), Cell(0, 8, (1,)),
            Cell(1, 0, (1,)), Cell(1, 8, (1,)),
            Cell(3, 0, (1,)), Cell(3, 6, (1,)), Cell(3, 7, (1,)), Cell(3, 8, (1,)),
            Cell(4, 2, (1,)), Cell(4, 6, (1,)), Cell(4, 7, (1,)), Cell(4, 8, (1,)),
            Cell(7, 7, (1,)), Cell(7, 8, (1,)),
        ]
        for cell in cells:
            sudoku.possible_values_grid[cell.line, cell.column, 1] = 1

        x_chains = XChains(sudoku)

        # When
        sudoku = x_chains(1)

        # Then
        invalid_cells = {Cell(4, 7, (1,)), Cell(4, 8, (1,))}
        for cell in invalid_cells:
            assert x_chains.sudoku.possible_values_grid[cell.line, cell.column, 1] == 0
        for cell in set(cells) - invalid_cells:
            assert x_chains.sudoku.possible_values_grid[cell.line, cell.column, 1] == 1
