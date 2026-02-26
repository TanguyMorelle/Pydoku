from collections.abc import Sequence

from pydoku.domain.models.sudoku import Sudoku
from pydoku.domain.models.updates.update import Update
from pydoku.domain.services.level_1.hidden_candidates_strategy import (
    HiddenCandidatesStrategy,
)


class CheckHiddenCandidates:
    def __init__(self, hidden_candidates_strategy: HiddenCandidatesStrategy) -> None:
        self.hidden_candidates_strategy = hidden_candidates_strategy

    def execute(self, sudoku: Sudoku) -> Sequence[Update]:
        updates = []
        updates.extend(self._check_in_rows(sudoku))
        updates.extend(self._check_in_columns(sudoku))
        updates.extend(self._check_in_blocks(sudoku))
        return updates

    def _check_in_rows(self, sudoku: Sudoku) -> Sequence[Update]:
        updates = []
        for row in range(9):
            updates.extend(
                self.hidden_candidates_strategy.check_for_hidden_row_sets(sudoku, row)
            )
        return updates

    def _check_in_columns(self, sudoku: Sudoku) -> Sequence[Update]:
        updates = []
        sudoku.transpose()
        for column in range(9):
            updates.extend(
                self.hidden_candidates_strategy.check_for_hidden_row_sets(
                    sudoku, column
                )
            )
        sudoku.transpose()
        return updates

    def _check_in_blocks(self, sudoku: Sudoku) -> Sequence[Update]:
        updates = []
        for block in range(9):
            updates.extend(
                self.hidden_candidates_strategy.check_for_hidden_block_sets(
                    sudoku, block
                )
            )
        return updates
