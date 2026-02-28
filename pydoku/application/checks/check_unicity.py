from pydoku.application.checks.check import Check
from pydoku.domain.models.sudoku import Sudoku
from pydoku.domain.models.updates.update import Update
from pydoku.domain.services.strategies.unicity_strategy import UnicityStrategy


class CheckUnicity(Check):
    def __init__(self, unicity_strategy: UnicityStrategy) -> None:
        self.strategy = unicity_strategy

    def execute(self, sudoku: Sudoku, early_stop: bool) -> list[Update]:
        cell_updates = self._get_cell_updates(sudoku)
        row_updates = self._get_row_updates(sudoku)
        column_updates = self._get_column_updates(sudoku)
        block_updates = self._get_block_updates(sudoku)
        return cell_updates + row_updates + column_updates + block_updates

    def _get_cell_updates(self, sudoku: Sudoku) -> list[Update]:
        updates: list[Update] = []
        for row in range(9):
            for column in range(9):
                updates.extend(self.strategy.unicity_in_cell(sudoku, row, column))
        return updates

    def _get_row_updates(self, sudoku: Sudoku) -> list[Update]:
        updates: list[Update] = []
        for row in range(9):
            updates.extend(self.strategy.unicity_in_row(sudoku, row))
        return updates

    def _get_column_updates(self, sudoku: Sudoku) -> list[Update]:
        updates: list[Update] = []
        with sudoku.transpose() as transpose_sudoku:
            for column in range(9):
                updates.extend(self.strategy.unicity_in_row(transpose_sudoku, column))
        return updates

    def _get_block_updates(self, sudoku: Sudoku) -> list[Update]:
        updates: list[Update] = []
        for block in range(9):
            updates.extend(self.strategy.unicity_in_blocks(sudoku, block))
        return updates
