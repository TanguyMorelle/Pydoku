import numpy as np

from pydoku.domain.exceptions.early_stop_exception import EarlyStopException
from pydoku.domain.models.cell import Cell
from pydoku.domain.models.sudoku import Sudoku
from pydoku.domain.models.updates.level_1.intersection_removal_update import (
    IntersectionRemovalTypes,
    IntersectionRemovalUpdate,
)
from pydoku.domain.models.updates.update import Update
from pydoku.utils.grid_tools import get_block_columns, get_block_rows


class BoxLineReduction:
    def check_in_block(
        self, sudoku: Sudoku, block: int, early_stop: bool
    ) -> list[Update]:
        updates = []
        missing_values = sudoku.grid.get_block(block).get_missing_values()
        block_columns = get_block_columns(block)
        for value in missing_values:
            for row in get_block_rows(block):
                (columns,) = np.where(sudoku.options.get_row_value(row, value) == 1)
                if len(columns) and len(set(columns) - set(block_columns)) == 0:
                    cells = sorted(Cell(row=row, column=column) for column in columns)
                    new_updates = self._get_updates(sudoku, cells, value, block, row)
                    if early_stop and len(new_updates) > 0:
                        raise EarlyStopException(updates=new_updates)
                    updates.extend(new_updates)
        return updates

    @staticmethod
    def _get_updates(
        sudoku: Sudoku, cells: list[Cell], value: int, block: int, row: int
    ) -> list[Update]:
        rows, columns = np.where(sudoku.options.get_block_value(block, value) == 1)
        option_updates = [
            Cell(row=r, column=c, values=[value])
            for (r, c) in zip(rows, columns)
            if r != row
        ]
        if len(option_updates) > 0:
            return [
                IntersectionRemovalUpdate(
                    cells=cells,
                    values=[value],
                    type=IntersectionRemovalTypes.BOX_LINE_REDUCTION,
                    options_updates=option_updates,
                    transposed=sudoku.transposed,
                )
            ]
        return []
