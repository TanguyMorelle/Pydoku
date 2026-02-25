from collections.abc import Sequence

import numpy as np

from pydoku.domain.models.cell import Cell
from pydoku.domain.models.sudoku import Sudoku
from pydoku.domain.models.units import Units
from pydoku.domain.models.updates.unicity_update import UnicityUpdate
from pydoku.utils.grid_tools import get_visibility


class UnicityStrategy:
    def unicity_in_cell(
        self, sudoku: Sudoku, row: int, column: int
    ) -> Sequence[UnicityUpdate]:
        (values,) = np.where(sudoku.options.get_cell(row, column) == 1)
        if len(values) == 1:
            return [
                UnicityUpdate(
                    unit=Units.CELL,
                    row=row,
                    column=column,
                    value=values[0],
                    options_updates=self._get_options_updates(
                        sudoku, row, column, values[0]
                    ),
                    transposed=sudoku.transposed,
                )
            ]
        return []

    def unicity_in_row(self, sudoku: Sudoku, row: int) -> Sequence[UnicityUpdate]:
        updates = []
        missing_values = sudoku.grid.get_row(row).get_missing_values()
        for value in missing_values:
            (columns,) = np.where(
                sudoku.options.get_row_value(row=row, value=value) == 1
            )
            if len(columns) == 1:
                updates.append(
                    UnicityUpdate(
                        unit=Units.ROW,
                        row=row,
                        column=columns[0],
                        value=value,
                        options_updates=self._get_options_updates(
                            sudoku, row, columns[0], value
                        ),
                        transposed=sudoku.transposed,
                    )
                )
        return updates

    def unicity_in_blocks(self, sudoku: Sudoku, block: int) -> Sequence[UnicityUpdate]:
        updates = []
        missing_values = sudoku.grid.get_block(block).get_missing_values()
        for value in missing_values:
            rows, columns = np.where(
                sudoku.options.get_block_value(block=block, value=value) == 1
            )
            if len(rows) == 1:
                row = rows[0] + 3 * (block // 3)
                column = columns[0] + (block % 3)
                updates.append(
                    UnicityUpdate(
                        unit=Units.BLOCK,
                        row=row,
                        column=column,
                        value=value,
                        options_updates=self._get_options_updates(
                            sudoku, row, column, value
                        ),
                        transposed=sudoku.transposed,
                    )
                )
        return updates

    @staticmethod
    def _get_options_updates(
        sudoku: Sudoku, row: int, column: int, value: int
    ) -> list[Cell]:
        positions = get_visibility((row, column))
        return [
            Cell(row=position[0], column=position[1], values=[value])
            for position in positions
            if sudoku.options.get_cell(*position)[value] == 1
        ]
