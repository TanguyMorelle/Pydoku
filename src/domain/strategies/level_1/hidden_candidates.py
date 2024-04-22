from typing import Any, Iterable

import numpy as np

from src.common.types import Position
from src.domain.cell import Cell
from src.domain.strategies.strategy import Strategy
from src.domain.strategies.strategy_object import StrategyObject
from src.domain.sudoku import Sudoku
from src.domain.units import Units
from src.domain.updates import ObjUpdate, Update
from src.utils.grid_tools import get_subsets


class HiddenCandidatesObject(StrategyObject):
    def __init__(
        self, transposed: bool, cells: list[Cell], values: Iterable[int]
    ) -> None:
        self.transposed = transposed
        self.cells = sorted(cells)
        self.values = values

    def realign(self) -> "HiddenCandidatesObject":
        if self.transposed:
            return HiddenCandidatesObject(
                False,
                [cell.transpose() for cell in self.cells],
                self.values,
            )
        return self

    def __str__(self) -> str:
        cells = " ".join([f"r{cell.row + 1}c{cell.column + 1}" for cell in self.cells])
        values = " ".join([str(value + 1) for value in self.values])
        return f"[UPD] hidden candidates [{cells}]@[{values}]\n"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, HiddenCandidatesObject):
            return False
        return self.__dict__ == other.__dict__


class HiddenCandidates(Strategy):
    def __init__(self, sudoku: Sudoku) -> None:
        self.sudoku = sudoku
        self.updates: list[Update] = []

    def execute(self) -> list[Update]:
        for _ in range(2):
            for row in range(9):
                self._check_for_hidden_row_sets(row)
            self.sudoku.transpose()
        for block in range(9):
            self._check_for_hidden_block_sets(block)
        return self.updates

    def _check_for_hidden_row_sets(self, row: int) -> None:
        missing_values = self.sudoku.get_missing_values(Units.ROW, row)
        for subsets in get_subsets(missing_values):
            for values in subsets:
                cells = self._get_cell_in_row_values_subset(row, values)
                if len(cells) == len(values):
                    self._update_sudoku(cells, values)

    def _get_cell_in_row_values_subset(
        self, row: int, values: tuple[int]
    ) -> list[Cell]:
        _, columns = np.where(
            self.sudoku.possible_values_grid.get_row(row, list(values)) == 1
        )
        return [Cell(row, column) for column in set(columns)]

    def _check_for_hidden_block_sets(self, block: int) -> None:
        missing_values = self.sudoku.get_missing_values(Units.BLOCK, block)
        for subsets in get_subsets(missing_values):
            for values in subsets:
                cells = self._get_cell_in_block_values_subset(block, values)
                if len(cells) == len(values):
                    self._update_sudoku(cells, values)

    def _get_cell_in_block_values_subset(
        self, block: int, values: tuple[int]
    ) -> list[Cell]:
        u, v = divmod(block, 3)
        rows, columns, _ = np.where(
            self.sudoku.possible_values_grid.get_block(block, list(values)) == 1
        )
        return [
            Cell(3 * u + row, 3 * v + column) for row, column in set(zip(rows, columns))
        ]

    def _update_sudoku(self, cells: list[Cell], values: tuple[int]) -> None:
        obj = HiddenCandidatesObject(self.sudoku.transposed, cells, values)
        positions = set([cell.position for cell in cells])
        cells_to_update = self._get_cells_to_update(positions, values)

        if len(cells_to_update):
            self.updates.append(
                ObjUpdate(
                    obj=obj,
                    transposed=self.sudoku.transposed,
                    possible_values_updates=sorted(cells_to_update),
                )
            )

    def _get_cells_to_update(
        self, positions: set[Position], values: Iterable[int]
    ) -> list[Cell]:
        cells_to_update = []
        for position in positions:
            (possible_values,) = np.where(
                self.sudoku.possible_values_grid[*position] == 1
            )
            values_to_remove = tuple(set(possible_values) - set(values))
            if len(values_to_remove):
                cells_to_update.append(Cell(*position, values_to_remove))
        return cells_to_update
