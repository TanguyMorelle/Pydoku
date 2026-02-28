import numpy as np

from pydoku.domain.exceptions.early_stop_exception import EarlyStopException
from pydoku.domain.models.cell import Cell
from pydoku.domain.models.sudoku import Sudoku
from pydoku.domain.models.updates.level_1.intersection_removal_update import (
    IntersectionRemovalTypes,
    IntersectionRemovalUpdate,
)
from pydoku.domain.models.updates.update import Update
from pydoku.utils.grid_tools import get_block_columns


class SingleLinePointingSets:
    def check_in_block(
        self, sudoku: Sudoku, block: int, early_stop: bool
    ) -> list[Update]:
        updates = []
        missing_values = sudoku.grid.get_block(block).get_missing_values()
        for value in missing_values:
            rows, columns = np.where(sudoku.options.get_block_value(block, value) == 1)
            if len(set(rows)) == 1 and len(columns) > 1:
                u, v = divmod(block, 3)
                row = rows[0]
                cells = sorted(
                    Cell(row=row + u, column=column + v) for column in columns
                )
                new_updates = self._get_updates(sudoku, cells, value, block, row)
                if early_stop and len(new_updates) > 0:
                    raise EarlyStopException(updates=new_updates)
                updates.extend(new_updates)
        return updates

    @staticmethod
    def _get_updates(
        sudoku: Sudoku, cells: list[Cell], value: int, block: int, row: int
    ) -> list[Update]:
        (columns,) = np.where(sudoku.options.get_row_value(row, value) == 1)
        option_updates = [
            Cell(row=row, column=column, values=[value])
            for column in columns
            if column not in get_block_columns(block)
        ]
        if len(option_updates) > 0:
            return [
                IntersectionRemovalUpdate(
                    cells=cells,
                    values=[value],
                    type=IntersectionRemovalTypes.SINGLE_LINE_POINTING_SETS,
                    options_updates=option_updates,
                    transposed=sudoku.transposed,
                )
            ]
        return []
