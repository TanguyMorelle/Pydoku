from typing import Optional

from src.adapters.solve_path_txt_handler import SolvePathTxtHandler
from src.domain.solve_path import SolvePath
from src.domain.strategies import StrategyLevels
from src.domain.sudoku import Sudoku
from src.domain.updates import Update


class Solver:
    def __init__(self, sudoku: Sudoku, name: Optional[str] = None) -> None:
        self.sudoku = sudoku
        self.solve_path = SolvePath(SolvePathTxtHandler())
        self.name = name or "sudoku"

    def solve(self) -> bool:
        result = self._solve()
        self.save()
        if result:
            print("solved")
        else:
            print(f"blocked at: {self.sudoku.progress}%")
        return result

    def _solve(self) -> bool:
        while not self.sudoku.solved:
            updates = self.step()
            if len(updates) == 0:
                return False
            self.sudoku.update(updates)
            self.solve_path.add(updates)
        return True

    def step(self) -> list[Update]:
        for strategy in StrategyLevels.strategies():
            updates = strategy(self.sudoku).execute()
            if len(updates):
                self.sudoku.realign()
                return updates
        return []

    def save(self) -> None:
        self.sudoku.save(self.name)
        self.solve_path.save(self.name)
