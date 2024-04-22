from src.domain.cell import Cell
from src.utils.grid_tools import get_visibility


class CellUTest:
    def test__attributes(self) -> None:
        # Given
        cell = Cell(5, 2, (5,))

        # Then
        assert cell.row == 5
        assert cell.column == 2
        assert cell.values == (5,)
        assert cell.position == (5, 2)
        assert cell.block == 3
        assert cell.visibility == get_visibility((5, 2))

    def test__equality__valid(self) -> None:
        # Given
        cell1 = Cell(1, 2)
        cell2 = Cell(1, 2)

        # Then
        assert cell1 == cell2

    def test__equality__invalid(self) -> None:
        # Given
        cell1 = Cell(1, 2)
        cell2 = Cell(3, 4)

        # Then
        assert cell1 != cell2

    def test__equality__invalid_type(self) -> None:
        # Given
        cell = Cell(1, 2, (2,))
        not_a_cell = [1, 1, (2,)]

        # Then
        assert cell != not_a_cell

    def test__transpose(self) -> None:
        # Given
        cell = Cell(1, 2, (3, 6))
        expected_cell = Cell(2, 1, (3, 6))

        # When
        transposed = cell.transpose()

        # Then
        assert transposed == expected_cell

    def test__hash(self) -> None:
        # Given
        cell = Cell(1, 2, (3,))

        # Then
        assert hash(cell) == hash((1, 2, (3,)))
