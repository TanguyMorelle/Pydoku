import numpy as np

from pydoku.domain.exceptions.early_stop_exception import EarlyStopException
from pydoku.domain.models.cell import Cell
from pydoku.domain.models.sudoku import Sudoku
from pydoku.domain.models.updates.level_1.intersection_removal_update import (
    IntersectionRemovalTypes,
    IntersectionRemovalUpdate,
)
from pydoku.domain.models.updates.update import Update


class MultiLinePointingSets:
    def check_in_block(
        self, sudoku: Sudoku, block: int, early_stop: bool
    ) -> list[Update]:
        updates = []
        missing_values = sudoku.grid.get_block(block).get_missing_values()
        other_row_blocks = list(set(range(block % 3, block % 3 + 3)) - {block % 3})
        for value in missing_values:
            rows_1, columns_1 = np.where(
                sudoku.options.get_block_value(other_row_blocks[0], value) == 1
            )
            rows_2, columns_2 = np.where(
                sudoku.options.get_block_value(other_row_blocks[1], value) == 1
            )
            rows = set(*rows_1, *rows_2)
            if len(rows) == 2 and len(rows_1) > 0 and len(rows_2) > 0:
                u1, v1 = divmod(other_row_blocks[0], 3)
                u2, v2 = divmod(other_row_blocks[1], 3)
                row = next(iter(set(range(3)) - rows))
                cells = sorted(
                    *[
                        Cell(row=row + u1, column=column + v1)
                        for (row, column) in zip(rows_1, columns_1)
                    ],
                    *[
                        Cell(row=row + u2, column=column + v2)
                        for (row, column) in zip(rows_2, columns_2)
                    ],
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
        u, v = divmod(block, 3)
        rows, columns = np.where(sudoku.options.get_block_value(block, value) == 1)
        option_updates = [
            Cell(row=r + u, column=c + v, values=[value])
            for r, c in zip(rows, columns)
            if r != row
        ]
        if len(option_updates) > 0:
            return [
                IntersectionRemovalUpdate(
                    cells=cells,
                    values=[value],
                    type=IntersectionRemovalTypes.MULTI_LINE_POINTING_SETS,
                    options_updates=option_updates,
                    transposed=sudoku.transposed,
                )
            ]
        return []
