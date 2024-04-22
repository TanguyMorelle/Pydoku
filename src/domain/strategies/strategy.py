from abc import ABC, abstractmethod

from src.domain.sudoku import Sudoku
from src.domain.updates import Update


class Strategy(ABC):

    @abstractmethod
    def __init__(self, sudoku: Sudoku) -> None: ...

    @abstractmethod
    def execute(self) -> list[Update]: ...
