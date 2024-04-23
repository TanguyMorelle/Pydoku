from typing import Any, Iterable

import numpy as np

from src.common.types import Position
from src.domain.cell import Cell
from src.domain.strategies.strategy import Strategy
from src.domain.strategies.strategy_object import StrategyObject
from src.domain.sudoku import Sudoku
from src.domain.updates import ObjUpdate, Update
from src.utils.grid_tools import get_subsets


class NakedCandidatesObject(StrategyObject):
    def __init__(
        self, transposed: bool, cells: list[Cell], values: Iterable[int]
    ) -> None:
        self.transposed = transposed
        self.cells = sorted(cells)
        self.values = values

    def realign(self) -> "NakedCandidatesObject":
        if self.transposed:
            return NakedCandidatesObject(
                False,
                [cell.transpose() for cell in self.cells],
                self.values,
            )
        return self

    def __str__(self) -> str:
        cells = " ".join([f"r{cell.row + 1}c{cell.column + 1}" for cell in self.cells])
        values = " ".join([str(value + 1) for value in self.values])
        return f"[UPD] naked candidates [{cells}]@[{values}]\n"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, NakedCandidatesObject):
            return False
        return self.__dict__ == other.__dict__


class NakedCandidates(Strategy):
    def __init__(self, sudoku: Sudoku) -> None:
        self.sudoku = sudoku
        self.updates: list[Update] = []

    def execute(self) -> list[Update]:
        for _ in range(2):
            for row in range(9):
                self._check_for_naked_groups_in_row(row)
            self.sudoku.transpose()
        for block in range(9):
            self._check_for_naked_groups_in_block(block)
        return self.updates

    def _check_for_naked_groups_in_row(self, row: int) -> None:
        x_pos, = np.where(self.sudoku.grid.get_row(row) == 0)
        empty_cells = [(row, column) for column in x_pos]
        self._check_for_naked_groups(empty_cells)

    def _check_for_naked_groups_in_block(self, block: int) -> None:
        u, v = divmod(block, 3)
        y_pos, x_pos = np.where(self.sudoku.grid.get_block(block) == 0)
        empty_cells = [(3 * u + i, 3 * v + j) for i, j in zip(y_pos, x_pos)]
        self._check_for_naked_groups(empty_cells)

    def _check_for_naked_groups(self, positions: list[Position]) -> None:
        cell_combinations = get_subsets(positions)
        for cell_combination_size in cell_combinations:
            for combination in cell_combination_size:
                possible_values: set[int] = set()
                for position in combination:
                    values, = np.where(self.sudoku.possible_values_grid[*position] == 1)
                    for value in values:
                        possible_values.add(value)
                if len(combination) == len(possible_values):
                    cells = [Cell(*position) for position in combination]
                    invalid_positions = set(positions) - set(combination)
                    self._update_sudoku(cells, invalid_positions, tuple(possible_values))

    def _update_sudoku(self, cells: list[Cell], invalid_positions: Iterable[Position], values: tuple[int, ...]) -> None:
        obj = NakedCandidatesObject(self.sudoku.transposed, cells, values)
        cells_to_update = self._get_cells_to_update(invalid_positions, values)

        if len(cells_to_update):
            self.updates.append(
                ObjUpdate(
                    obj=obj,
                    transposed=self.sudoku.transposed,
                    possible_values_updates=sorted(cells_to_update),
                )
            )

    def _get_cells_to_update(
        self, positions: Iterable[Position], values: tuple[int, ...]
    ) -> list[Cell]:
        cells_to_update = []
        for position in positions:
            (possible_values,) = np.where(
                self.sudoku.possible_values_grid[*position] == 1
            )
            values_to_remove = tuple(set(possible_values).intersection(set(values)))
            if len(values_to_remove):
                cells_to_update.append(Cell(*position, values_to_remove))
        return cells_to_update
