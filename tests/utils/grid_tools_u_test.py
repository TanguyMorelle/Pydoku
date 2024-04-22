from src.utils.grid_tools import get_block, get_subsets, get_visibility


class GridToolsUTest:
    def test__get_visibility_should_return_visibility(self) -> None:
        # Given
        position = (5, 7)
        expected_visible_positions = [
            (0, 7),
            (1, 7),
            (2, 7),
            (3, 7),
            (4, 7),
            (6, 7),
            (7, 7),
            (8, 7),
            (5, 0),
            (5, 1),
            (5, 2),
            (5, 3),
            (5, 4),
            (5, 5),
            (5, 6),
            (5, 8),
            (3, 6),
            (3, 8),
            (4, 6),
            (4, 8),
        ]

        # When
        result = get_visibility(position)

        # Then
        assert len(result) == len(expected_visible_positions)
        assert set(result) - set(expected_visible_positions) == set()

    def test__get_block_should_return_block(self) -> None:
        # Given
        position = (5, 7)
        expected_block = 5

        # When
        result = get_block(position)

        # Then
        assert result == expected_block

    def test__get_subset_should_return_subset(self) -> None:
        # Given
        position = (5, 7)
        elements = list(range(5))

        # When
        result = list(get_subsets(elements))

        # Then
        assert len(result) == 3
        assert result[0] == [
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 2),
            (1, 3),
            (1, 4),
            (2, 3),
            (2, 4),
            (3, 4),
        ]

        assert result[1] == [
            (0, 1, 2),
            (0, 1, 3),
            (0, 1, 4),
            (0, 2, 3),
            (0, 2, 4),
            (0, 3, 4),
            (1, 2, 3),
            (1, 2, 4),
            (1, 3, 4),
            (2, 3, 4),
        ]

        assert result[2] == [
            (0, 1, 2, 3),
            (0, 1, 2, 4),
            (0, 1, 3, 4),
            (0, 2, 3, 4),
            (1, 2, 3, 4),
        ]
