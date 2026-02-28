from pydoku.application.checks.check import Check
from pydoku.domain.exceptions.early_stop_exception import EarlyStopException
from pydoku.domain.models.sudoku import Sudoku
from pydoku.domain.models.updates.update import Update
from pydoku.domain.services.strategies.level_1.hidden_candidates_strategy import (
    HiddenCandidatesStrategy,
)


class CheckHiddenCandidates(Check):
    def __init__(self, hidden_candidates_strategy: HiddenCandidatesStrategy) -> None:
        self.hidden_candidates_strategy = hidden_candidates_strategy

    def execute(self, sudoku: Sudoku, early_stop: bool) -> list[Update]:
        updates = []
        try:
            updates.extend(self._check_in_rows(sudoku, early_stop))
            updates.extend(self._check_in_columns(sudoku, early_stop))
            updates.extend(self._check_in_blocks(sudoku, early_stop))
        except EarlyStopException as e:
            updates = e.updates
        return updates

    def _check_in_rows(self, sudoku: Sudoku, early_stop: bool) -> list[Update]:
        updates = []
        for row in range(9):
            updates.extend(
                self.hidden_candidates_strategy.check_for_hidden_row_sets(
                    sudoku, row, early_stop
                )
            )
        return updates

    def _check_in_columns(self, sudoku: Sudoku, early_stop: bool) -> list[Update]:
        updates = []
        with sudoku.transpose() as transposed_sudoku:
            for column in range(9):
                updates.extend(
                    self.hidden_candidates_strategy.check_for_hidden_row_sets(
                        transposed_sudoku, column, early_stop
                    )
                )
        return updates

    def _check_in_blocks(self, sudoku: Sudoku, early_stop: bool) -> list[Update]:
        updates = []
        for block in range(9):
            updates.extend(
                self.hidden_candidates_strategy.check_for_hidden_block_sets(
                    sudoku, block, early_stop
                )
            )
        return updates
