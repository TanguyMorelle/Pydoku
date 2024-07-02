from src.domain.cell import Cell
from src.domain.strategies.level_1.hidden_candidates import (
    HiddenCandidates,
    HiddenCandidatesObject,
)
from src.domain.updates import ObjUpdate
from tests.fixtures.fake_sudoku_factory import fake_sudoku_factory


class HiddenCandidatesUTest:
    def test__find_hidden_candidates_in_row(self) -> None:
        # Given
        sudoku = fake_sudoku_factory(
            cell_overrides=[
                Cell(4, 5, (1,)),
                Cell(4, 7, (3,)),
            ],
            possible_values_overrides=[
                Cell(4, 0, (3, 6, 7, 8)),
                Cell(4, 1, (3, 7, 8)),
                Cell(4, 2, (3, 6)),
                Cell(4, 3, (1, 3, 4, 5, 6, 7)),
                Cell(4, 4, (3, 6, 7)),
                Cell(4, 6, (1, 3, 5, 8)),
                Cell(4, 8, (1, 3, 4, 6, 7, 8)),
            ],
        )
        sudoku.possible_values_grid[list(set(range(9)) - {4}), :, :] = 1
        strategy = HiddenCandidates(sudoku)

        # When
        updates = strategy.execute()

        # Then
        expected = [
            ObjUpdate(
                obj=HiddenCandidatesObject(
                    False,
                    [
                        Cell(4, 3),
                        Cell(4, 6),
                        Cell(4, 8),
                    ],
                    (1, 4, 5),
                ),
                transposed=False,
                possible_values_updates=[
                    Cell(4, 3, (3, 6, 7)),
                    Cell(4, 6, (3, 8)),
                    Cell(4, 8, (3, 6, 7, 8)),
                ],
            )
        ]
        assert updates == expected

    def test__find_hidden_candidates_in_block(self) -> None:
        # Given
        sudoku = fake_sudoku_factory(
            possible_values_overrides=[
                Cell(3, 3, (0, 2, 3, 5, 6, 7, 8)),
                Cell(3, 4, (2, 6, 7)),
                Cell(3, 5, (2, 3, 5, 6, 7, 8)),
                Cell(4, 3, (1, 2, 6, 7)),
                Cell(4, 4, (1, 2, 4, 6, 7)),
                Cell(4, 5, (1, 2, 4, 6, 7)),
                Cell(5, 3, (0, 2, 3, 6, 7, 8)),
                Cell(5, 4, (2, 4, 6, 7)),
                Cell(5, 5, (2, 3, 4, 6, 7, 8)),
            ],
        )
        positions = {
            (3, 3),
            (3, 4),
            (3, 5),
            (4, 3),
            (4, 4),
            (4, 5),
            (5, 3),
            (
                5,
                4,
            ),
            (5, 5),
        }
        for position in set((i, j) for i in range(9) for j in range(9)) - set(
            positions
        ):
            sudoku.possible_values_grid[*position, :] = 1
        strategy = HiddenCandidates(sudoku)

        # When
        updates = strategy.execute()

        # Then
        expected = [
            ObjUpdate(
                obj=HiddenCandidatesObject(
                    False,
                    [
                        Cell(3, 3),
                        Cell(3, 5),
                        Cell(5, 3),
                        Cell(5, 5),
                    ],
                    (0, 3, 5, 8),
                ),
                transposed=False,
                possible_values_updates=[
                    Cell(3, 3, (2, 6, 7)),
                    Cell(3, 5, (2, 6, 7)),
                    Cell(5, 3, (2, 6, 7)),
                    Cell(5, 5, (2, 4, 6, 7)),
                ],
            )
        ]
        assert updates == expected


class HiddenCandidatesObjectUTest:
    def test__stringify(self) -> None:
        # Given
        transposed = True
        cells = [Cell(0, 1, (4, 5, 6, 7)), Cell(0, 2, (4, 5, 6)), Cell(0, 5, (4, 5, 6))]
        values = [4, 5, 6]
        obj = HiddenCandidatesObject(transposed, cells, values)

        # When
        representation = str(obj)

        # Then
        assert representation == "[UPD] hidden candidates [r1c2 r1c3 r1c6]@[5 6 7]\n"
        assert obj != 10

    def test__realign_not_transposed_should_be_self(self) -> None:
        # Given
        transposed = False
        cells = [Cell(0, 1, (4, 5, 6, 7)), Cell(0, 2, (4, 5, 6)), Cell(0, 5, (4, 5, 6))]
        values = [4, 5, 6]
        obj = HiddenCandidatesObject(transposed, cells, values)

        # When
        result = obj.realign()

        # Then
        assert result == obj

    def test__realign_transposed_should_be_realigned(self) -> None:
        # Given
        transposed = True
        cells = [Cell(0, 1, (4, 5, 6, 7)), Cell(0, 2, (4, 5, 6)), Cell(0, 5, (4, 5, 6))]
        values = [4, 5, 6]
        obj = HiddenCandidatesObject(transposed, cells, values)

        # When
        result = obj.realign()

        # Then
        assert result == HiddenCandidatesObject(
            False, [cell.transpose() for cell in cells], values
        )
