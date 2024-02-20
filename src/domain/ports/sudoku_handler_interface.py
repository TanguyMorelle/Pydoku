from abc import ABC, abstractmethod
from typing import Any

from src.domain.sudoku import Sudoku


class SudokuHandlerInterface(ABC):
    @abstractmethod
    def load(self, entrypoint: Any) -> Sudoku: ...

    @abstractmethod
    def save(self, sudoku: Sudoku, name: str) -> None: ...
