from abc import ABC, abstractmethod

from src.domain.sudoku import Sudoku
from src.domain.updates import Update


class Strategy(ABC):
    def __init__(self, sudoku: Sudoku) -> None:
        self.sudoku = sudoku

    @abstractmethod
    def execute(self) -> list[Update]: ...
