from typing import Optional

import numpy as np

from src.adapters.sudoku_seq_handler import SudokuSeqHandler
from src.domain.cell import Cell
from src.domain.grid import PossibleValuesGrid, ValuesGrid
from src.domain.ports.sudoku_handler_interface import SudokuHandlerInterface
from src.domain.sudoku import Sudoku


def fake_sudoku_factory(
    cell_overrides: Optional[list[Cell]] = None,
    possible_values_overrides: Optional[list[Cell]] = None,
    loader: Optional[SudokuHandlerInterface] = SudokuSeqHandler(),
) -> Sudoku:
    grid = ValuesGrid(np.zeros((9, 9)))
    for cell in cell_overrides or []:
        grid[cell.row][cell.column] = cell.values[0]
    sudoku = Sudoku(grid, loader)
    sudoku.possible_values_grid = PossibleValuesGrid(np.zeros((9, 9, 9)))
    for cell in possible_values_overrides or []:
        for value in range(9):
            if value in cell.values:
                sudoku.possible_values_grid[*cell.position, value] = 1
    return sudoku
