import numpy as np
import pytest

from pydoku.domain.models.cell import Cell
from pydoku.domain.models.updates.level_1.naked_candidates_update import (
    NakedCandidatesUpdate,
)
from pydoku.domain.services.level_1.naked_candidates_strategy import (
    NakedCandidatesStrategy,
)
from tests.fixtures.sudoku_test_builder import SudokuTestBuilder


class TestCheckNakedCandidates:
    @pytest.fixture
    def strategy(self) -> NakedCandidatesStrategy:
        return NakedCandidatesStrategy()

    def test_naked_triple_in_row(
        self, strategy: NakedCandidatesStrategy, sudoku_builder: SudokuTestBuilder
    ) -> None:
        # GIVEN
        sudoku = sudoku_builder.with_initial_grid(
            np.array(
                [
                    [0, 7, 0, 4, 0, 8, 0, 2, 9],
                    [0, 0, 2, 0, 0, 0, 0, 0, 4],
                    [8, 5, 4, 0, 2, 0, 0, 0, 7],
                    [0, 0, 8, 3, 7, 4, 2, 0, 0],
                    [0, 2, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 3, 2, 6, 1, 7, 0, 0],
                    [0, 0, 0, 0, 9, 3, 6, 1, 2],
                    [2, 0, 0, 0, 0, 0, 4, 0, 3],
                    [1, 3, 0, 6, 4, 2, 0, 7, 0],
                ]
            )
        ).build()
        expected_updates = [
            NakedCandidatesUpdate(
                cells=[
                    Cell(row=4, column=3),
                    Cell(row=4, column=4),
                    Cell(row=4, column=5),
                ],
                values=(4, 7, 8),
                options_updates=[
                    Cell(row=4, column=0, values=[4, 8]),
                    Cell(row=4, column=2, values=[4, 8]),
                    Cell(row=4, column=6, values=[4, 7, 8]),
                    Cell(row=4, column=7, values=[4, 7, 8]),
                    Cell(row=4, column=8, values=[4, 7]),
                ],
                transposed=False,
            )
        ]

        # WHEN
        updates = strategy.check_for_naked_groups_in_row(sudoku, 4)

        # THEN
        assert len(updates) == 1
        assert updates == expected_updates

    def test_naked_pair_in_block(
        self, strategy: NakedCandidatesStrategy, sudoku_builder: SudokuTestBuilder
    ) -> None:
        # GIVEN
        sudoku = sudoku_builder.with_initial_grid(
            np.array(
                [
                    [4, 0, 0, 0, 0, 0, 0, 3, 8],
                    [0, 0, 2, 0, 0, 4, 1, 0, 0],
                    [0, 9, 5, 3, 0, 0, 2, 4, 0],
                    [0, 7, 0, 6, 0, 9, 0, 0, 4],
                    [0, 2, 0, 0, 0, 1, 0, 7, 0],
                    [6, 0, 0, 7, 0, 3, 0, 9, 0],
                    [0, 5, 7, 0, 0, 8, 3, 0, 0],
                    [0, 0, 3, 9, 0, 0, 4, 0, 0],
                    [2, 4, 0, 0, 0, 0, 0, 0, 9],
                ]
            )
        ).build()
        expected_updates = [
            NakedCandidatesUpdate(
                cells=[Cell(row=0, column=1), Cell(row=0, column=2)],
                values=(0, 5),
                options_updates=[
                    Cell(row=1, column=1, values=[5]),
                    Cell(row=2, column=0, values=[0]),
                ],
                transposed=False,
            )
        ]

        # WHEN
        updates = strategy.check_for_naked_groups_in_block(sudoku, 0)

        # THEN
        assert len(updates) == 1
        assert updates == expected_updates
