from collections.abc import Sequence

from pydoku.domain.models.sudoku import Sudoku
from pydoku.domain.models.updates.update import Update
from pydoku.domain.services.level_1.naked_candidates_strategy import (
    NakedCandidatesStrategy,
)


class CheckNakedCandidates:
    def __init__(self, naked_candidates_strategy: NakedCandidatesStrategy) -> None:
        self.naked_candidates_strategy = naked_candidates_strategy

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
                self.naked_candidates_strategy.check_for_naked_groups_in_row(
                    sudoku, row
                )
            )
        return updates

    def _check_in_columns(self, sudoku: Sudoku) -> Sequence[Update]:
        updates = []
        sudoku.transpose()
        for row in range(9):
            updates.extend(
                self.naked_candidates_strategy.check_for_naked_groups_in_row(
                    sudoku, row
                )
            )
        sudoku.transpose()
        return updates

    def _check_in_blocks(self, sudoku: Sudoku) -> Sequence[Update]:
        updates = []
        for block in range(9):
            updates.extend(
                self.naked_candidates_strategy.check_for_naked_groups_in_block(
                    sudoku, block
                )
            )
        return updates
