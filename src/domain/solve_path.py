from typing import TYPE_CHECKING

from src.domain.updates import Update

if TYPE_CHECKING:
    from src.domain.ports.solve_path_handler_interface import SolvePathHandlerInterface


class SolvePath:
    def __init__(self, handler: "SolvePathHandlerInterface") -> None:
        self.path: list[list[Update]] = []
        self.handler = handler

    def add(self, updates: list[Update]) -> None:
        self.path.append(updates)

    def save(self, name: str) -> None:
        self.handler.save(self, name)
