from abc import ABC, abstractmethod

from pydoku.domain.models.sudoku import Sudoku
from pydoku.domain.models.updates.update import Update


class SudokuUpdater[T: Update](ABC):
    @staticmethod
    @abstractmethod
    def apply_update(step: int, sudoku: Sudoku, update: T) -> None: ...
