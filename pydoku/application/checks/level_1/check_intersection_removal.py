from pydoku.application.checks.check import Check
from pydoku.domain.exceptions.early_stop_exception import EarlyStopException
from pydoku.domain.models.sudoku import Sudoku
from pydoku.domain.models.updates.update import Update
from pydoku.domain.services.strategies.level_1.intersection_removal import (
    BoxLineReduction,
    MultiLinePointingSets,
    SingleLinePointingSets,
)


class CheckIntersectionRemoval(Check):
    def __init__(
        self,
        box_line_reduction: BoxLineReduction,
        single_line_pointing_sets: SingleLinePointingSets,
        multi_lines_pointing_sets: MultiLinePointingSets,
    ) -> None:
        self.box_line_reduction = box_line_reduction
        self.single_line_pointing_sets = single_line_pointing_sets
        self.multi_lines_pointing_sets = multi_lines_pointing_sets

    def execute(self, sudoku: Sudoku, early_stop: bool) -> list[Update]:
        updates = []
        try:
            updates.extend(self._check_in_rows(sudoku, early_stop))
            updates.extend(self._check_in_columns(sudoku, early_stop))
        except EarlyStopException as e:
            updates = e.updates
        return updates

    def _check_in_rows(self, sudoku: Sudoku, early_stop: bool) -> list[Update]:
        return self._check_in_blocks(sudoku, early_stop)

    def _check_in_columns(self, sudoku: Sudoku, early_stop: bool) -> list[Update]:
        with sudoku.transpose() as transposed_sudoku:
            return self._check_in_blocks(transposed_sudoku, early_stop)

    def _check_in_blocks(self, sudoku: Sudoku, early_stop: bool) -> list[Update]:
        updates = []
        for block in range(9):
            updates.extend(
                self.single_line_pointing_sets.check_in_block(sudoku, block, early_stop)
            )
        return updates
