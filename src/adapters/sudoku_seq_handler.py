import re
from pathlib import Path

import numpy as np

from src.adapters.exceptions import InvalidInputException
from src.domain.ports.sudoku_handler_interface import SudokuHandlerInterface
from src.domain.sudoku import Sudoku


class SudokuSeqHandler(SudokuHandlerInterface):
    @staticmethod
    def _validate_sequence(sequence: str) -> None:
        if len(sequence) != 81:
            raise InvalidInputException

    def load(self, sequence: str) -> Sudoku:
        self._validate_sequence(sequence)
        formatted_sequence = re.sub(r"\D", "0", sequence)
        data = np.array([int(char) for char in formatted_sequence]).reshape(9, 9)
        return Sudoku(data, self)

    def save(self, sudoku: Sudoku, name: str | Path) -> None:
        filename = f"{name}_seq.txt"
        sequence = re.sub(r"\D", "", str(sudoku.grid.flatten()))
        with open(filename, "w") as file:
            file.write(sequence)
