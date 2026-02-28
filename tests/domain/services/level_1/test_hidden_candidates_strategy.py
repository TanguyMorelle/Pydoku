import numpy as np
import pytest

from pydoku.domain.exceptions.early_stop_exception import EarlyStopException
from pydoku.domain.models.cell import Cell
from pydoku.domain.models.updates.level_1.hidden_candidates_update import (
    HiddenCandidatesUpdate,
)
from pydoku.domain.services.strategies.level_1.hidden_candidates_strategy import (
    HiddenCandidatesStrategy,
)
from tests.fixtures.sudoku_test_builder import SudokuTestBuilder


class TestCheckHiddenCandidates:
    @pytest.fixture
    def strategy(self) -> HiddenCandidatesStrategy:
        return HiddenCandidatesStrategy()

    def test_hidden_triple_in_row(
        self, strategy: HiddenCandidatesStrategy, sudoku_builder: SudokuTestBuilder
    ) -> None:
        # GIVEN
        sudoku = sudoku_builder.with_initial_grid(
            np.array(
                [
                    [0, 0, 0, 0, 0, 1, 0, 3, 0],
                    [2, 3, 1, 0, 9, 0, 0, 0, 0],
                    [0, 6, 5, 0, 0, 3, 1, 0, 0],
                    [6, 7, 8, 9, 2, 4, 3, 0, 0],
                    [1, 0, 3, 0, 5, 0, 0, 0, 6],
                    [0, 0, 0, 1, 3, 6, 7, 0, 0],
                    [0, 0, 9, 3, 6, 0, 5, 7, 0],
                    [0, 0, 6, 0, 1, 9, 8, 4, 3],
                    [3, 0, 0, 0, 0, 0, 0, 0, 0],
                ]
            )
        ).build()
        expected_updates = [
            HiddenCandidatesUpdate(
                cells=[
                    Cell(row=0, column=3),
                    Cell(row=0, column=6),
                    Cell(row=0, column=8),
                ],
                values=(1, 4, 5),
                options_updates=[
                    Cell(row=0, column=3, values=[3, 6, 7]),
                    Cell(row=0, column=6, values=[3, 8]),
                    Cell(row=0, column=8, values=[3, 6, 7, 8]),
                ],
                transposed=False,
            )
        ]

        # WHEN
        updates = strategy.check_for_hidden_row_sets(sudoku, 0, False)

        # THEN
        assert len(updates) == 1
        assert updates == expected_updates

    def test_hidden_pair_in_block(
        self, strategy: HiddenCandidatesStrategy, sudoku_builder: SudokuTestBuilder
    ) -> None:
        # GIVEN
        sudoku = sudoku_builder.with_initial_grid(
            np.array(
                [
                    [7, 2, 0, 4, 0, 8, 0, 3, 0],
                    [0, 8, 0, 0, 0, 0, 0, 4, 7],
                    [4, 0, 1, 0, 7, 6, 8, 0, 2],
                    [8, 1, 0, 7, 3, 9, 0, 0, 0],
                    [0, 0, 0, 8, 5, 1, 0, 0, 0],
                    [0, 0, 0, 2, 6, 4, 0, 8, 0],
                    [2, 0, 9, 6, 8, 0, 4, 1, 3],
                    [3, 4, 0, 0, 0, 0, 0, 0, 8],
                    [1, 6, 8, 9, 4, 3, 2, 7, 5],
                ]
            )
        ).build()
        expected_updates = [
            HiddenCandidatesUpdate(
                cells=[Cell(row=3, column=2), Cell(row=4, column=2)],
                values=(1, 3),
                options_updates=[
                    Cell(row=3, column=2, values=[4, 5]),
                    Cell(row=4, column=2, values=[2, 5, 6]),
                ],
                transposed=False,
            ),
            HiddenCandidatesUpdate(
                cells=[
                    Cell(row=4, column=0),
                    Cell(row=3, column=2),
                    Cell(row=4, column=2),
                ],
                values=(1, 3, 5),
                options_updates=[
                    Cell(row=3, column=2, values=[4]),
                    Cell(row=4, column=0, values=[8]),
                    Cell(row=4, column=2, values=[2, 6]),
                ],
                transposed=False,
            ),
        ]

        # WHEN
        updates = strategy.check_for_hidden_block_sets(sudoku, 3, False)

        # THEN
        assert len(updates) == 2
        assert updates == expected_updates

    def test_hidden_pair_in_block_with_early_stop(
        self, strategy: HiddenCandidatesStrategy, sudoku_builder: SudokuTestBuilder
    ) -> None:
        # GIVEN
        sudoku = sudoku_builder.with_initial_grid(
            np.array(
                [
                    [7, 2, 0, 4, 0, 8, 0, 3, 0],
                    [0, 8, 0, 0, 0, 0, 0, 4, 7],
                    [4, 0, 1, 0, 7, 6, 8, 0, 2],
                    [8, 1, 0, 7, 3, 9, 0, 0, 0],
                    [0, 0, 0, 8, 5, 1, 0, 0, 0],
                    [0, 0, 0, 2, 6, 4, 0, 8, 0],
                    [2, 0, 9, 6, 8, 0, 4, 1, 3],
                    [3, 4, 0, 0, 0, 0, 0, 0, 8],
                    [1, 6, 8, 9, 4, 3, 2, 7, 5],
                ]
            )
        ).build()
        expected_updates = [
            HiddenCandidatesUpdate(
                cells=[Cell(row=3, column=2), Cell(row=4, column=2)],
                values=(1, 3),
                options_updates=[
                    Cell(row=3, column=2, values=[4, 5]),
                    Cell(row=4, column=2, values=[2, 5, 6]),
                ],
                transposed=False,
            ),
        ]

        # WHEN
        with pytest.raises(EarlyStopException) as e:
            strategy.check_for_hidden_block_sets(sudoku, 3, True)
        updates = e.value.updates

        # THEN
        assert len(updates) == 1
        assert updates == expected_updates
