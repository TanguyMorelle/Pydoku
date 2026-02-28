from copy import deepcopy
from typing import Any

from src.domain.models.sudoku import Sudoku
import numpy as np

from src.domain.services.strategies_level_1.hidden_candidates import HiddenCandidates
from src.domain.services.strategies_level_1.intersection_removal import IntersectionRemoval
from src.domain.services.strategies_level_1.naked_candidates import NakedCandidates
from src.domain.services.strategies_level_2.remote_pairs import RemotePairs
from src.domain.services.strategies_level_2.single_chains import SingleChains
from src.domain.services.strategies_level_2.swordfish import Swordfish
from src.domain.services.strategies_level_2.x_wing import XWing
from src.domain.services.strategies_level_2.xyz_wing import XYZWing
from src.domain.services.strategies_level_2.y_wing import YWing
from src.domain.services.strategies_level_3.x_chain import XChains
from src.domain.services.strategies_level_3.x_cycles import XCycles
from src.domain.services.strategies_level_3.xy_chains import XYChains


class Solver:
    def __init__(self, sudoku: Sudoku, available_strategies: list[Any] = []) -> None:
        self.sudoku = sudoku
        self.initialisation()
        self.initial_grid = self.sudoku.possible_values_grid
        self.available_strategies = available_strategies

    @classmethod
    def from_csv(cls, file: str, available_strategies: list[Any] = []) -> "Solver":
        data = np.genfromtxt(file, delimiter=',')
        grid = Sudoku(data)
        return cls(grid, available_strategies)

    def save_grid_status(self) -> None:
        np.savetxt('result.csv', self.sudoku.grid.astype(int), delimiter=",", fmt="%.1s")

    def initialisation(self) -> None:
        for _ in range(2):
            for i in range(9):
                self._update_line_options(i)
            self.sudoku.transpose()
        for y in range(3):
            for x in range(3):
                self._update_block_options(y, x)

    def _update_line_options(self, i: int) -> None:
        for value in range(9):
            if value + 1 in self.sudoku.grid[i]:
                self.sudoku.possible_values_grid[i, :, value] = 0

    def _update_block_options(self, y: int, x: int) -> None:
        u, v = 3 * y, 3 * x
        for value in range(9):
            if value + 1 in self.sudoku.grid[u:u + 3, v:v + 3]:
                self.sudoku.possible_values_grid[u:u + 3, v:v + 3, value] = 0

    def solve(self) -> None:
        if self._solve():
            print("solved")
        else:
            print(f"blocked at: {self.sudoku.get_progress()}%")
        self.save_grid_status()

    def _solve(self) -> bool:
        while not self.sudoku.is_solved():
            soft_lock = not self.step()
            if soft_lock:
                return False
        return True

    def step(self) -> bool:
        self.initial_grid = deepcopy(self.sudoku.possible_values_grid)
        strategy_levels = [
            self.strategies_level_1,
            self.strategies_level_2,
            self.strategies_level_3
        ]
        for level in strategy_levels:
            level()
            if self.updated_initial_grid():
                return True
        return False

    def updated_initial_grid(self) -> bool:
        if not np.array_equal(self.initial_grid, self.sudoku.possible_values_grid):
            return True
        return False

    # check_forces
    def strategies_level_1(self) -> None:
        strategies = [
            IntersectionRemoval,
            NakedCandidates,
            HiddenCandidates
        ]
        for strategy in strategies:
            self._execute_strategy(strategy)

    def strategies_level_2(self) -> None:
        strategies = [
            XWing,
            YWing,
            XYZWing,
            Swordfish,
            RemotePairs,
            SingleChains
        ]
        for strategy in strategies:
            self._execute_strategy(strategy)

    def strategies_level_3(self) -> None:
        strategies = [
            XChains,
            XCycles,
            XYChains
        ]
        for strategy in strategies:
            self._execute_strategy(strategy)

    def _execute_strategy(self, strategy: Any) -> None:
        if len(self.available_strategies) == 0 or (
                len(self.available_strategies) > 0 and strategy in self.available_strategies):
            self.sudoku = strategy(self.sudoku)()
            self.sudoku.set_values()
            if self.updated_initial_grid():
                return
