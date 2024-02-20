import numpy as np

from src.domain.cell import Cell
from src.domain.strategies.base import Unicity
from src.domain.units import Units
from src.domain.updates import GridUpdate
from tests.fixtures.fake_sudoku_factory import fake_sudoku_factory

print(np.zeros((9, 9)))


class UnicityUTest:
    def test_should_return_unique_cell_in_cell(self) -> None:
        # Given
        cell_1 = Cell(2, 7, (3,))
        cell_2 = Cell(6, 5, (2,))
        positions = {(line, column) for line in range(9) for column in range(9)} - {
            cell_1.position,
            cell_2.position,
        }
        possible_values_cells = [
            Cell(*position, (2, 3, 4) if position[0] < 5 else (4, 5))
            for position in positions
        ]
        possible_values_update_cell_1 = [
            Cell(*position, (3,)) for position in cell_1.visibility if position[0] < 5
        ]
        possible_values_update_cell_2 = [
            Cell(*position, (2,)) for position in cell_2.visibility if position[0] < 5
        ]

        possible_values_cells += [cell_1, cell_2]
        sudoku = fake_sudoku_factory(possible_values_overrides=possible_values_cells)
        unicity = Unicity(sudoku)

        # When
        grid_updates = unicity.execute()

        # Then
        assert len(grid_updates) == 2
        assert isinstance(grid_updates[0], GridUpdate)
        assert grid_updates[0].unit == Units.CELL
        assert grid_updates[0].cell == cell_1
        assert (
            set(grid_updates[0].possible_values_updates)
            - set(possible_values_update_cell_1)
            == set()
        )
        assert grid_updates[1].unit == Units.CELL
        assert grid_updates[1].cell == cell_2
        assert (
            set(grid_updates[1].possible_values_updates)
            - set(possible_values_update_cell_2)
            == set()
        )

    def test_should_return_unique_cell_in_line(self) -> None:
        # Given
        columns = set(range(9))
        cell_1 = Cell(3, 4, (2, 3, 5))
        cell_2 = Cell(5, 7, (2, 3, 5))
        possible_values_cells_column_1 = [
            Cell(3, column, (3, 5)) for column in columns - {4}
        ]
        possible_values_cells_column_2 = [
            Cell(5, column, (2, 5)) for column in columns - {7}
        ]
        possible_values_cells_column_3 = [
            Cell(4, column, (2, 3, 5)) for column in columns
        ]
        possible_values_cells = [
            cell_1,
            cell_2,
            *possible_values_cells_column_1,
            *possible_values_cells_column_2,
            *possible_values_cells_column_3,
        ]

        sudoku = fake_sudoku_factory(possible_values_overrides=possible_values_cells)
        unicity = Unicity(sudoku)

        # When
        grid_updates = unicity.execute()

        # Then
        assert len(grid_updates) == 2
        assert grid_updates[0].unit == Units.ROW
        assert grid_updates[0].cell == Cell(3, 4, (2,))
        s1 = {
            Cell(4, 3, (2,)),
            Cell(4, 4, (2,)),
            Cell(4, 5, (2,)),
            Cell(5, 3, (2,)),
            Cell(5, 4, (2,)),
            Cell(5, 5, (2,)),
        }
        assert set(grid_updates[0].possible_values_updates) - s1 == set()
        assert grid_updates[1].unit == Units.ROW
        assert grid_updates[1].cell == Cell(5, 7, (3,))
        s2 = {
            Cell(3, 6, (3,)),
            Cell(3, 7, (3,)),
            Cell(3, 8, (3,)),
            Cell(4, 6, (3,)),
            Cell(4, 7, (3,)),
            Cell(4, 8, (3,)),
        }
        assert set(grid_updates[1].possible_values_updates) - s2 == set()

    def test_should_return_unique_cell_in_block(self) -> None:
        # Given
        lines = range(3, 6)
        columns = range(3, 9)
        cell_1 = Cell(3, 0, (2, 3, 5))
        possible_values_cells_column_1 = [
            Cell(line, column, (3, 5))
            for line in set(lines) - {3}
            for column in range(3)
        ]
        possible_values_cells_column_2 = [
            Cell(line, column, (2, 3, 5)) for line in lines for column in columns
        ]
        possible_values_cells_column_3 = [
            Cell(line, column, (2, 3, 5))
            for line in set(range(9)) - set(range(3, 6))
            for column in range(3)
        ]
        possible_values_cells = [
            cell_1,
            *possible_values_cells_column_1,
            *possible_values_cells_column_2,
            *possible_values_cells_column_3,
        ]

        sudoku = fake_sudoku_factory(possible_values_overrides=possible_values_cells)
        unicity = Unicity(sudoku)

        # When
        grid_updates = unicity.execute()

        # Then
        assert len(grid_updates) == 1
        assert grid_updates[0].unit == Units.BLOCK
        assert grid_updates[0].cell == Cell(3, 0, (2,))
        s1 = {
            *[Cell(3, column, (2,)) for column in range(3, 9)],
            *[Cell(line, 0, (2,)) for line in set(range(9)) - set(range(3, 6))],
        }
        assert set(grid_updates[0].possible_values_updates) - s1 == set()
