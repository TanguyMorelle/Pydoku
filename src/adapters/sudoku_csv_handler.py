from pathlib import Path

import numpy as np

from src.adapters.exceptions import InvalidInputException
from src.domain.ports.sudoku_handler_interface import SudokuHandlerInterface
from src.domain.sudoku import Sudoku


class SudokuCsvHandler(SudokuHandlerInterface):
    @staticmethod
    def _validate_grid(grid: np.ndarray) -> None:
        checks = [
            grid.shape == (9, 9),
            grid.dtype.kind in {"i", "u", "f"},
            np.all((grid <= 9) & (grid >= 0)),
        ]
        if not all(checks):
            raise InvalidInputException

    def load(self, filename: str) -> Sudoku:
        if not filename.endswith(".csv"):
            raise InvalidInputException
        grid = np.genfromtxt(filename, delimiter=",")
        self._validate_grid(grid)
        return Sudoku(grid.astype(int), self)

    def save(self, sudoku: Sudoku, name: str | Path) -> None:
        filename = f"{name}_grid.csv"
        np.savetxt(filename, sudoku.grid.astype(int), delimiter=",", fmt="%.1s")
