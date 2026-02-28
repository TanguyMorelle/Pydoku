from typing import override

from pydoku.domain.models.sudoku import Sudoku
from pydoku.domain.models.updates.level_1.hidden_candidates_update import (
    HiddenCandidatesUpdate,
)
from pydoku.domain.services.updaters.sudoku_updater import SudokuUpdater


class HiddenCandidatesUpdater(SudokuUpdater[HiddenCandidatesUpdate]):
    @staticmethod
    @override
    def apply_update(step: int, sudoku: Sudoku, update: HiddenCandidatesUpdate) -> None:
        sudoku.add_update(step, update)
        for option in update.options_updates:
            for value in option.values or []:
                sudoku.options[option.row, option.column, value] = 0
