from copy import deepcopy

from src.domain.cell import Cell
from src.domain.units import Units
from src.domain.updates import GridUpdate


class GridUpdateUTest:
    def test__equality_valid(self) -> None:
        # Given
        cell = Cell(4, 2, (1,))
        possible_values_updates = [
            Cell(4, 5, (1,)),
            Cell(4, 6, (1,)),
        ]
        update_1 = GridUpdate(
            unit=Units.ROW,
            transposed=False,
            cell=cell,
            possible_values_updates=possible_values_updates,
        )
        update_2 = GridUpdate(
            unit=Units.ROW,
            transposed=False,
            cell=deepcopy(cell),
            possible_values_updates=deepcopy(possible_values_updates),
        )

        # When
        assert update_1 == update_2

    def test__equality_invalid(self) -> None:
        # Given
        cell = Cell(4, 2, (1,))
        possible_values_updates = [
            Cell(4, 5, (1,)),
            Cell(4, 6, (1,)),
        ]
        update_1 = GridUpdate(
            unit=Units.ROW,
            transposed=False,
            cell=cell,
            possible_values_updates=possible_values_updates,
        )
        update_2 = GridUpdate(
            unit=Units.ROW,
            transposed=True,
            cell=deepcopy(cell),
            possible_values_updates=deepcopy(possible_values_updates),
        )

        # When
        assert update_1 != update_2

    def test__equality_invalid_object(self) -> None:
        # Given
        cell = Cell(4, 2, (1,))
        possible_values_updates = [
            Cell(4, 5, (1,)),
            Cell(4, 6, (1,)),
        ]
        update_1 = GridUpdate(
            unit=Units.ROW,
            transposed=False,
            cell=cell,
            possible_values_updates=possible_values_updates,
        )
        update_2 = [5]

        # When
        assert update_1 != update_2

    def test__row_message(self) -> None:
        # Given
        cell = Cell(4, 2, (1,))
        possible_values_updates = [
            Cell(4, 5, (1,)),
            Cell(4, 6, (1,)),
        ]
        update = GridUpdate(
            unit=Units.ROW,
            transposed=False,
            cell=cell,
            possible_values_updates=possible_values_updates,
        )

        # When
        message = str(update)

        # Then
        assert message == (
            "[SET] unique option 2 [r5] @ r5c3\n"
            "    | removes 2 @ r5c6\n"
            "    | removes 2 @ r5c7\n"
        )

    def test__column_message(self) -> None:
        # Given
        cell = Cell(4, 2, (1,))
        possible_values_updates = [
            Cell(2, 2, (1,)),
            Cell(6, 2, (1,)),
        ]
        update = GridUpdate(
            unit=Units.COLUMN,
            transposed=False,
            cell=cell,
            possible_values_updates=possible_values_updates,
        )

        # When
        message = str(update)

        # Then
        assert message == (
            "[SET] unique option 2 [c3] @ r5c3\n"
            "    | removes 2 @ r3c3\n"
            "    | removes 2 @ r7c3\n"
        )

    def test__block_message(self) -> None:
        # Given
        cell = Cell(4, 2, (1,))
        possible_values_updates = [
            Cell(3, 1, (1,)),
            Cell(5, 2, (1,)),
        ]
        update = GridUpdate(
            unit=Units.BLOCK,
            transposed=False,
            cell=cell,
            possible_values_updates=possible_values_updates,
        )

        # When
        message = str(update)

        # Then
        assert message == (
            "[SET] unique option 2 [b4] @ r5c3\n"
            "    | removes 2 @ r4c2\n"
            "    | removes 2 @ r6c3\n"
        )

    def test__cell_message(self) -> None:
        # Given
        cell = Cell(4, 2, (1,))
        possible_values_updates = [
            Cell(3, 1, (1,)),
            Cell(5, 2, (1,)),
        ]
        update = GridUpdate(
            unit=Units.CELL,
            transposed=False,
            cell=cell,
            possible_values_updates=possible_values_updates,
        )

        # When
        message = str(update)

        # Then
        assert message == (
            "[SET] unique option 2 @ r5c3\n"
            "    | removes 2 @ r4c2\n"
            "    | removes 2 @ r6c3\n"
        )

    def test__realign_not_transposed(self) -> None:
        # Given
        cell = Cell(4, 2, (1,))
        possible_values_updates = [
            Cell(4, 5, (1,)),
            Cell(4, 6, (1,)),
        ]
        update = GridUpdate(
            unit=Units.ROW,
            transposed=False,
            cell=cell,
            possible_values_updates=possible_values_updates,
        )

        # When
        realigned_update = update.realign()

        # Then
        assert realigned_update == update

    def test__realign_row_transposed(self) -> None:
        # Given
        cell = Cell(4, 2, (1,))
        possible_values_updates = [
            Cell(4, 5, (1,)),
            Cell(4, 6, (1,)),
        ]
        update = GridUpdate(
            unit=Units.ROW,
            transposed=True,
            cell=cell,
            possible_values_updates=possible_values_updates,
        )

        # When
        realigned_update = update.realign()

        # Then
        assert realigned_update.unit is Units.COLUMN
        assert realigned_update.transposed is False
        assert realigned_update.cell == Cell(2, 4, (1,))
        assert realigned_update.possible_values_updates == [
            Cell(5, 4, (1,)),
            Cell(6, 4, (1,)),
        ]

    def test__realign_column_transposed(self) -> None:
        # Given
        cell = Cell(4, 2, (1,))
        possible_values_updates = [
            Cell(4, 5, (1,)),
            Cell(4, 6, (1,)),
        ]
        update = GridUpdate(
            unit=Units.COLUMN,
            transposed=True,
            cell=cell,
            possible_values_updates=possible_values_updates,
        )

        # When
        realigned_update = update.realign()

        # Then
        assert realigned_update.unit is Units.ROW
        assert realigned_update.transposed is False
        assert realigned_update.cell == Cell(2, 4, (1,))
        assert realigned_update.possible_values_updates == [
            Cell(5, 4, (1,)),
            Cell(6, 4, (1,)),
        ]

    def test__realign_block_transposed(self) -> None:
        # Given
        cell = Cell(4, 2, (1,))
        possible_values_updates = [
            Cell(4, 5, (1,)),
            Cell(4, 6, (1,)),
        ]
        update = GridUpdate(
            unit=Units.BLOCK,
            transposed=True,
            cell=cell,
            possible_values_updates=possible_values_updates,
        )

        # When
        realigned_update = update.realign()

        # Then
        assert realigned_update.unit is Units.BLOCK
        assert realigned_update.transposed is False
        assert realigned_update.cell == Cell(2, 4, (1,))
        assert realigned_update.possible_values_updates == [
            cell.transpose() for cell in possible_values_updates
        ]
