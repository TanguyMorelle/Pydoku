from collections.abc import Iterable, Sequence

import numpy as np

from pydoku.domain.exceptions.early_stop_exception import EarlyStopException
from pydoku.domain.models.cell import Cell
from pydoku.domain.models.sudoku import Sudoku
from pydoku.domain.models.types import Position
from pydoku.domain.models.updates.level_1.naked_candidates_update import (
    NakedCandidatesUpdate,
)
from pydoku.domain.models.updates.update import Update
from pydoku.utils.grid_tools import get_subsets


class NakedCandidatesStrategy:
    def check_for_naked_groups_in_row(
        self, sudoku: Sudoku, row: int, early_stop: bool
    ) -> Sequence[NakedCandidatesUpdate]:
        (columns,) = np.where(sudoku.grid.get_row(row) == 0)
        empty_cells = [(row, column) for column in columns]
        return self._check_for_naked_groups(sudoku, empty_cells, early_stop)

    def check_for_naked_groups_in_block(
        self, sudoku: Sudoku, block: int, early_stop: bool
    ) -> Sequence[NakedCandidatesUpdate]:
        u, v = divmod(block, 3)
        rows, columns = np.where(sudoku.grid.get_block(block) == 0)
        empty_cells = [(3 * u + i, 3 * v + j) for i, j in zip(rows, columns)]
        return self._check_for_naked_groups(sudoku, empty_cells, early_stop)

    def _check_for_naked_groups(
        self, sudoku: Sudoku, positions: list[Position], early_stop: bool
    ) -> Sequence[NakedCandidatesUpdate]:
        updates = []
        cell_combinations = get_subsets(positions, max_size=len(positions) - 1)
        for cell_combination_size in cell_combinations:
            for combination in cell_combination_size:
                options = self._get_combination_value_options(sudoku, combination)
                if len(combination) == len(options):
                    new_updates = self._get_updates(
                        sudoku=sudoku,
                        combination=combination,
                        positions=positions,
                        options=options,
                    )
                    if early_stop:
                        raise EarlyStopException(updates=new_updates)
                    updates.extend(new_updates)
        return updates

    @staticmethod
    def _get_combination_value_options(
        sudoku: Sudoku, combination: list[Position]
    ) -> list[int]:
        possible_values: set[int] = set()
        for position in combination:
            (values,) = np.where(sudoku.options.get_cell(*position) == 1)
            for value in values:
                possible_values.add(value)
        return list(possible_values)

    @staticmethod
    def _get_cells_to_update(
        sudoku: Sudoku, positions: Iterable[Position], values: list[int]
    ) -> list[Cell]:
        cells_to_update = []
        for position in positions:
            (possible_values,) = np.where(sudoku.options.get_cell(*position) == 1)
            values_to_remove = list(set(possible_values).intersection(set(values)))
            if len(values_to_remove):
                cells_to_update.append(
                    Cell(row=position[0], column=position[1], values=values_to_remove)
                )
        return cells_to_update

    def _get_updates(
        self,
        sudoku: Sudoku,
        combination: Iterable[Position],
        positions: Iterable[Position],
        options: list[int],
    ) -> list[Update]:
        cells = [Cell(row=position[0], column=position[1]) for position in combination]
        invalid_positions = set(positions) - set(combination)
        cells_to_update = self._get_cells_to_update(sudoku, invalid_positions, options)
        if len(cells_to_update):
            return [
                NakedCandidatesUpdate(
                    cells=sorted(cells),
                    values=sorted(options),
                    options_updates=sorted(cells_to_update),
                    transposed=sudoku.transposed,
                )
            ]
        return []
