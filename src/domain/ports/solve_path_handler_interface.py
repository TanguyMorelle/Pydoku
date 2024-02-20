from abc import ABC, abstractmethod

from src.domain.solve_path import SolvePath


class SolvePathHandlerInterface(ABC):
    @abstractmethod
    def save(self, solve_path: SolvePath, name: str) -> None: ...
