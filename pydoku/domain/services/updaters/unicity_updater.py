from typing import override

import numpy as np

from pydoku.domain.models.sudoku import Sudoku
from pydoku.domain.models.updates.unicity_update import UnicityUpdate
from pydoku.domain.services.updaters.sudoku_updater import SudokuUpdater


class UnicityUpdater(SudokuUpdater[UnicityUpdate]):
    @staticmethod
    @override
    def apply_update(step: int, sudoku: Sudoku, update: UnicityUpdate) -> None:
        sudoku.add_update(step, update)
        sudoku.grid[update.row, update.column] = update.value + 1
        sudoku.options[update.row, update.column] = np.zeros((9,), dtype=int)
        for option in update.options_updates:
            for value in option.values or []:
                sudoku.options[option.row, option.column, value] = 0
