import numpy as np
import pytest

from pydoku.domain.models.cell import Cell
from pydoku.domain.models.units import Units
from pydoku.domain.models.updates.unicity_update import UnicityUpdate
from pydoku.domain.services.unicity_strategy import UnicityStrategy
from pydoku.utils.grid_tools import get_block, get_visibility
from tests.fixtures.sudoku_test_builder import SudokuTestBuilder


class TestUnicityStrategy:
    @pytest.fixture
    def strategy(self) -> UnicityStrategy:
        return UnicityStrategy()

    def test_unicity_in_cell_with_single_option(
        self, strategy: UnicityStrategy, sudoku_builder: SudokuTestBuilder
    ) -> None:
        # GIVEN
        sudoku = sudoku_builder.with_initial_grid_row(
            2, np.array([1, 2, 3, 0, 6, 7, 8, 9, 4])
        ).build()
        expected_options_update = [
            Cell(row=row, column=column, values=[4])
            for (row, column) in get_visibility((2, 3))
            if row != 2
        ]
        expected_updates = [
            UnicityUpdate(
                unit=Units.CELL,
                row=2,
                column=3,
                value=4,
                options_updates=expected_options_update,
                transposed=False,
            )
        ]

        # WHEN
        updates = strategy.unicity_in_cell(sudoku, 2, 3)

        # THEN
        assert len(updates) == len(expected_updates)
        assert updates[0] == expected_updates[0]

    def test_unicity_in_cell_with_single_option_transposed(
        self, strategy: UnicityStrategy, sudoku_builder: SudokuTestBuilder
    ) -> None:
        # GIVEN
        sudoku = sudoku_builder.with_initial_grid_column(
            2, np.array([1, 2, 3, 0, 6, 7, 8, 9, 4])
        ).build()
        sudoku.transpose()
        expected_options_update = [
            Cell(row=row, column=column, values=[4])
            for (row, column) in get_visibility((2, 3))
            if row != 2
        ]
        expected_updates = [
            UnicityUpdate(
                unit=Units.CELL,
                row=2,
                column=3,
                value=4,
                options_updates=expected_options_update,
                transposed=True,
            )
        ]

        # WHEN
        updates = strategy.unicity_in_cell(sudoku, 2, 3)

        # THEN
        assert len(updates) == len(expected_updates)
        assert updates[0] == expected_updates[0]

    def test_unicity_in_cell_with_multiple_options(
        self, strategy: UnicityStrategy, sudoku_builder: SudokuTestBuilder
    ) -> None:
        # GIVEN
        sudoku = sudoku_builder.with_initial_grid_row(
            2, np.array([1, 2, 3, 0, 0, 7, 8, 9, 4])
        ).build()

        # WHEN
        updates = strategy.unicity_in_cell(sudoku, 2, 3)

        # THEN
        assert len(updates) == 0

    def test_unicity_in_row_with_unique_positions(
        self, strategy: UnicityStrategy, sudoku_builder: SudokuTestBuilder
    ) -> None:
        # GIVEN
        sudoku = sudoku_builder.with_initial_grid_row(
            2, np.array([1, 2, 3, 0, 6, 7, 8, 9, 4])
        ).build()
        expected_options_update = [
            Cell(row=row, column=column, values=[4])
            for (row, column) in get_visibility((2, 3))
            if row != 2
        ]
        expected_updates = [
            UnicityUpdate(
                unit=Units.ROW,
                row=2,
                column=3,
                value=4,
                options_updates=expected_options_update,
                transposed=False,
            )
        ]

        # WHEN
        updates = strategy.unicity_in_row(sudoku, 2)

        # THEN
        assert len(updates) == len(expected_updates)
        assert updates[0] == expected_updates[0]

    def test_unicity_in_row_with_unique_positions_transposed(
        self, strategy: UnicityStrategy, sudoku_builder: SudokuTestBuilder
    ) -> None:
        # GIVEN
        sudoku = sudoku_builder.with_initial_grid_column(
            2, np.array([1, 2, 3, 0, 5, 7, 6, 9, 4])
        ).build()
        sudoku.transpose()
        expected_options_update = [
            Cell(row=row, column=column, values=[7])
            for (row, column) in get_visibility((2, 3))
            if row != 2
        ]
        expected_updates = [
            UnicityUpdate(
                unit=Units.ROW,
                row=2,
                column=3,
                value=7,
                options_updates=expected_options_update,
                transposed=True,
            )
        ]

        # WHEN
        updates = strategy.unicity_in_row(sudoku, 2)

        # THEN
        assert len(updates) == len(expected_updates)
        assert updates[0] == expected_updates[0]

    def test_unicity_in_row_with_no_unique_values(
        self, strategy: UnicityStrategy, sudoku_builder: SudokuTestBuilder
    ) -> None:
        # GIVEN
        sudoku = sudoku_builder.with_initial_grid_row(
            5, np.array([1, 2, 3, 0, 0, 7, 8, 9, 4])
        ).build()

        # WHEN
        updates = strategy.unicity_in_row(sudoku, 5)

        # THEN
        assert len(updates) == 0

    def test_unicity_in_blocks_with_unique_position(
        self, strategy: UnicityStrategy, sudoku_builder: SudokuTestBuilder
    ) -> None:
        # GIVEN
        sudoku = sudoku_builder.with_initial_grid(
            np.array(
                [
                    [1, 2, 3, 0, 0, 0, 0, 0, 0],
                    [4, 6, 7, 0, 0, 0, 0, 0, 0],
                    [8, 9, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                ]
            )
        ).build()
        expected_options_update = [
            Cell(row=row, column=column, values=[4])
            for (row, column) in get_visibility((2, 2))
            if get_block((row, column)) != 0
        ]
        expected_updates = [
            UnicityUpdate(
                unit=Units.BLOCK,
                row=2,
                column=2,
                value=4,
                options_updates=expected_options_update,
                transposed=False,
            )
        ]

        # WHEN
        updates = strategy.unicity_in_blocks(sudoku, 0)

        # THEN
        assert len(updates) == len(expected_updates)
        assert updates[0] == expected_updates[0]

    def test_unicity_in_blocks_with_unique_position_transposed(
        self, strategy: UnicityStrategy, sudoku_builder: SudokuTestBuilder
    ) -> None:
        # GIVEN
        sudoku = sudoku_builder.with_initial_grid(
            np.array(
                [
                    [0, 0, 0, 0, 0, 0, 1, 2, 3],
                    [0, 0, 0, 0, 0, 0, 4, 6, 0],
                    [0, 0, 0, 0, 0, 0, 8, 9, 7],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                ]
            )
        ).build()
        sudoku.transpose()
        expected_options_update = [
            Cell(row=row, column=column, values=[4])
            for (row, column) in get_visibility((8, 1))
            if get_block((row, column)) != 6
        ]
        expected_updates = [
            UnicityUpdate(
                unit=Units.BLOCK,
                row=8,
                column=1,
                value=4,
                options_updates=expected_options_update,
                transposed=True,
            )
        ]

        # WHEN
        updates = strategy.unicity_in_blocks(sudoku, 6)

        # THEN
        assert len(updates) == len(expected_updates)
        assert updates[0] == expected_updates[0]

    def test_unicity_in_blocks_with_no_unique_values(
        self, strategy: UnicityStrategy, sudoku_builder: SudokuTestBuilder
    ) -> None:
        # GIVEN
        sudoku = sudoku_builder.with_initial_grid(
            np.array(
                [
                    [0, 0, 0, 1, 2, 3, 0, 0, 0],
                    [0, 0, 0, 4, 6, 0, 0, 0, 0],
                    [0, 0, 0, 8, 9, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                ]
            )
        ).build()

        # WHEN
        updates = strategy.unicity_in_blocks(sudoku, 1)

        # THEN
        assert len(updates) == 0
