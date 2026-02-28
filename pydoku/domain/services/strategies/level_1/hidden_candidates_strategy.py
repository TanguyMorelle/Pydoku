from collections.abc import Iterable, Sequence

import numpy as np

from pydoku.domain.exceptions.early_stop_exception import EarlyStopException
from pydoku.domain.models.cell import Cell
from pydoku.domain.models.sudoku import Sudoku
from pydoku.domain.models.types import Position
from pydoku.domain.models.updates.level_1.hidden_candidates_update import (
    HiddenCandidatesUpdate,
)
from pydoku.domain.models.updates.update import Update
from pydoku.utils.grid_tools import get_subsets


class HiddenCandidatesStrategy:
    def check_for_hidden_row_sets(
        self, sudoku: Sudoku, row: int, early_stop: bool
    ) -> Sequence[HiddenCandidatesUpdate]:
        updates = []
        missing_values = sudoku.grid.get_row(row).get_missing_values()
        for subsets in get_subsets(missing_values):
            for values in subsets:
                cells = self._get_cell_in_row_values_subset(sudoku, row, values)
                if len(cells) == len(values):
                    new_updates = self._get_updates(
                        sudoku=sudoku,
                        cells=cells,
                        values=values,
                    )
                    if early_stop:
                        raise EarlyStopException(updates=new_updates)
                    updates.extend(new_updates)
        return updates

    def check_for_hidden_block_sets(
        self, sudoku: Sudoku, block: int, early_stop: bool
    ) -> Sequence[HiddenCandidatesUpdate]:
        updates = []
        missing_values = sudoku.grid.get_block(block).get_missing_values()
        for subsets in get_subsets(missing_values):
            for values in subsets:
                cells = self._get_cell_in_block_values_subset(sudoku, block, values)
                if len(cells) == len(values):
                    new_updates = self._get_updates(
                        sudoku=sudoku,
                        cells=cells,
                        values=values,
                    )
                    if early_stop:
                        raise EarlyStopException(updates=new_updates)
                    updates.extend(new_updates)
        return updates

    @staticmethod
    def _get_cell_in_row_values_subset(
        sudoku: Sudoku, row: int, values: list[int]
    ) -> list[Cell]:
        columns, _ = np.where(sudoku.options.get_row(row)[:, values] == 1)
        return [Cell(row=row, column=column) for column in set(columns)]

    @staticmethod
    def _get_cell_in_block_values_subset(
        sudoku: Sudoku, block: int, values: list[int]
    ) -> list[Cell]:
        u, v = divmod(block, 3)
        rows, columns, _ = np.where(sudoku.options.get_block(block)[:, :, values] == 1)
        return [
            Cell(row=3 * u + row, column=3 * v + column)
            for row, column in set(zip(rows, columns))
        ]

    @staticmethod
    def _get_cells_to_update(
        sudoku: Sudoku, positions: Iterable[Position], values: Iterable[int]
    ) -> list[Cell]:
        cells_to_update = []
        for position in positions:
            (options,) = np.where(sudoku.options[*position, :] == 1)
            values_to_remove = list(set(options) - set(values))
            if len(values_to_remove):
                cells_to_update.append(
                    Cell(row=position[0], column=position[1], values=values_to_remove)
                )
        return cells_to_update

    def _get_updates(
        self, sudoku: Sudoku, cells: list[Cell], values: list[int]
    ) -> list[Update]:
        positions = {cell.position for cell in cells}
        cells_to_update = self._get_cells_to_update(sudoku, positions, values)
        if len(cells_to_update):
            return [
                HiddenCandidatesUpdate(
                    cells=sorted(cells),
                    values=sorted(values),
                    options_updates=sorted(cells_to_update),
                    transposed=sudoku.transposed,
                )
            ]
        return []
