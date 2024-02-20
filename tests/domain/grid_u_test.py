import numpy as np

from src.domain.grid import PossibleValuesGrid, ValuesGrid


class ValueGridUTest:
    def test__get_row(self) -> None:
        # Given
        grid = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        values_grid = ValuesGrid(grid)

        # When
        row = values_grid.get_row(1)

        # Then
        assert np.array_equal(row, np.array([4, 5, 6]))

    def test__get_column(self) -> None:
        # Given
        grid = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        values_grid = ValuesGrid(grid)

        # When
        column = values_grid.get_column(1)

        # Then
        assert np.array_equal(column, np.array([2, 5, 8]))

    def test__get_block(self) -> None:
        # Given
        grid = np.array(list([n**2 + m for m in range(9)] for n in range(9)))
        values_grid = ValuesGrid(grid)

        # When
        block = values_grid.get_block(4)

        # Then
        assert np.array_equal(
            block, np.array([[12, 13, 14], [19, 20, 21], [28, 29, 30]])
        )


class PossibleValuesGridUTest:
    def test__get_row_no_value(self) -> None:
        # Given
        grid = np.array(list([[m] * 9] * 9 for m in range(9)))
        possible_values_grid = PossibleValuesGrid(grid)

        # When
        row = possible_values_grid.get_row(4)

        # Then
        assert np.array_equal(row, np.array([[4] * 9] * 9))

    def test__get_column_no_value(self) -> None:
        # Given
        grid = np.array(list([[m] * 9] * 9 for m in range(9))).transpose(1, 0, 2)
        possible_values_grid = PossibleValuesGrid(grid)

        # When
        column = possible_values_grid.get_column(4)

        # Then
        assert np.array_equal(column, np.array([[4] * 9] * 9))

    def test__get_block_no_value(self) -> None:
        # Given
        grid = np.array(list([[n**2 + m] * 9 for m in range(9)] for n in range(9)))
        possible_values_grid = PossibleValuesGrid(grid)

        # When
        block = possible_values_grid.get_block(4)

        # Then
        assert np.array_equal(
            block,
            np.array(
                [
                    [[12] * 9, [13] * 9, [14] * 9],
                    [[19] * 9, [20] * 9, [21] * 9],
                    [[28] * 9, [29] * 9, [30] * 9],
                ]
            ),
        )

    def test__get_row_with_value(self) -> None:
        # Given
        grid = np.array(list([[m**2 + i for i in range(9)]] * 9 for m in range(9)))
        possible_values_grid = PossibleValuesGrid(grid)

        # When
        row = possible_values_grid.get_row(4, 5)

        # Then
        assert np.array_equal(row, np.array([21] * 9))

    def test__get_column_with_value(self) -> None:
        # Given
        grid = np.array(
            list([[m**2 + i for i in range(9)]] * 9 for m in range(9))
        ).transpose(1, 0, 2)
        possible_values_grid = PossibleValuesGrid(grid)

        # When
        row = possible_values_grid.get_column(4, 5)

        # Then
        assert np.array_equal(row, np.array([21] * 9))

    def test__get_block_with_value(self) -> None:
        # Given
        grid = np.array(
            list(
                [[m**3 + i**2 + j for i in range(9)] for j in range(9)]
                for m in range(9)
            )
        )
        possible_values_grid = PossibleValuesGrid(grid)

        # When
        block = possible_values_grid.get_block(4, 5)

        # Then
        assert np.array_equal(
            block, np.array([[55, 56, 57], [92, 93, 94], [153, 154, 155]])
        )
