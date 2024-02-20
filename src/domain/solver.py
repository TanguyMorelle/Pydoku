from typing import Optional

from src.domain.data_loader import DataLoader
from src.domain.sudoku import Sudoku
from src.strategies import StrategyLevels
from src.utils.updates import GridUpdate, PossibleValuesUpdate, Update


class Solver:
    def __init__(self, sudoku: Sudoku, name: Optional[str] = None) -> None:
        self.sudoku = sudoku
        self.name = name or ""
        self.solve_path: list[list[Update]] = []
        self._setup()

    def save_grid_status(self) -> None:
        DataLoader.save_grid(self.sudoku, self.name)
        DataLoader.save_solve_path(self.solve_path, self.name)

    def _setup(self) -> None:
        for _ in range(2):
            for i in range(9):
                self._update_row_options(i)
            self.sudoku.transpose()
        for block in range(9):
            self._update_block_options(block)

    def _update_row_options(self, row: int) -> None:
        for value in range(9):
            if value + 1 in self.sudoku.grid.get_row(row):
                self.sudoku.possible_values_grid.get_row(row, value)[:] = 0

    def _update_block_options(self, block: int) -> None:
        for value in range(9):
            if value + 1 in self.sudoku.grid.get_block(block):
                self.sudoku.possible_values_grid.get_block(block, value)[:] = 0

    def solve(self) -> bool:
        result = self._solve()
        self.save_grid_status()
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
            self.update_sudoku(updates)
        return True

    def step(self) -> list[Update]:
        for strategy_level in StrategyLevels.values():
            for strategy in strategy_level.values():
                updates = strategy(self.sudoku).execute()
                self.solve_path.append(updates)
                if len(updates):
                    self.sudoku.realign()
                    return updates
        return []

    def update_sudoku(self, updates: list[Update]) -> None:
        for update in list(map(lambda u: u.realign(), updates)):
            if isinstance(update, GridUpdate):
                self.sudoku.update_grid(update)
            elif isinstance(update, PossibleValuesUpdate):
                self.sudoku.update_possible_values_grid(update)
            else:
                raise ValueError("Invalid update type")
