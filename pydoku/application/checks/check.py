from abc import ABC, abstractmethod

from pydoku.domain.models.sudoku import Sudoku
from pydoku.domain.models.updates.update import Update


class Check(ABC):
    @abstractmethod
    def execute(self, sudoku: Sudoku, early_stop: bool) -> list[Update]: ...
