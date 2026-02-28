from pydoku.application.checks.check import Check
from pydoku.domain.models.sudoku import Sudoku
from pydoku.domain.models.updates.update import Update
from pydoku.domain.services.updaters.updater_factory import apply_update


class Solver:
    def __init__(
        self, sudoku: Sudoku, available_checks: list[Check], step: int | None = None
    ) -> None:
        self.sudoku = sudoku
        self.available_checks = available_checks
        self.step = step or 1

    def solve(self) -> None:
        pass

    def solve_step(self, early_stop: bool = False) -> bool:
        updates = self._run_checks(early_stop)
        self._apply_updates(updates)
        return len(updates) > 0

    def _run_checks(self, early_stop: bool) -> list[Update]:
        for check in self.available_checks:
            updates = check.execute(self.sudoku, early_stop)
            if updates:
                return updates
        return []

    def _apply_updates(self, updates: list[Update]) -> None:
        for update in updates:
            apply_update(self.step, self.sudoku, update)
