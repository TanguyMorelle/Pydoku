from src.domain.cell import Cell
from src.domain.strategies.level_1.naked_candidates import NakedCandidates, NakedCandidatesObject
from src.domain.updates import ObjUpdate
from tests.fixtures.fake_sudoku_factory import fake_sudoku_factory


class NakedCandidatesUTest:
    def test__find_naked_candidates_in_row(self) -> None:
        # Given
        sudoku = fake_sudoku_factory(
            cell_overrides=[
                Cell(2, 1, (9,)),
                Cell(2, 2, (3,)),
                Cell(2, 3, (8,)),
                Cell(2, 6, (2,)),
                Cell(2, 7, (4,)),
            ],
            possible_values_overrides=[
                Cell(2, 0, (0, 6, 7)),
                Cell(2, 4, (0, 5, 6, 7)),
                Cell(2, 5, (5, 6)),
                Cell(2, 8, (5, 6)),
            ],
        )
        sudoku.possible_values_grid[list(set(range(9)) - {2}), :, :] = 1
        strategy = NakedCandidates(sudoku)

        # When
        updates = strategy.execute()

        # Then
        expected = [
            ObjUpdate(
                obj=NakedCandidatesObject(
                    False,
                    [
                        Cell(2, 5),
                        Cell(2, 8),
                    ],
                    (5, 6),
                ),
                transposed=False,
                possible_values_updates=[
                    Cell(2, 0, (6,)),
                    Cell(2, 4, (5, 6)),
                ],
            )
        ]
        assert updates == expected

    def test__find_naked_candidates_in_block(self) -> None:
        # Given
        sudoku = fake_sudoku_factory(
            cell_overrides=[
                Cell(6, 3, (5,)),
                Cell(6, 4, (6,)),
                Cell(6, 5, (3,)),
                Cell(7, 3, (2,)),
                Cell(8, 4, (1,)),
            ],
            possible_values_overrides=[
                Cell(7, 4, (3, 6)),
                Cell(7, 5, (6, 7, 8)),
                Cell(8, 3, (3, 6)),
                Cell(8, 5, (6, 7, 8)),
            ],
        )
        positions = [(y, x) for y in range(6, 9) for x in range(3, 6)]
        for position in set((y, x) for y in range(9) for x in range(9) if (y, x) not in positions):
            sudoku.possible_values_grid[*position, :] = 1
        strategy = NakedCandidates(sudoku)

        # When
        strategy._check_for_naked_groups_in_block(7)
        updates = strategy.updates

        # Then
        expected = [
            ObjUpdate(
                obj=NakedCandidatesObject(
                    False,
                    [
                        Cell(7, 4),
                        Cell(8, 3),
                    ],
                    (3, 6),
                ),
                transposed=False,
                possible_values_updates=[
                    Cell(7, 5, (6,)),
                    Cell(8, 5, (6,)),
                ],
            )
        ]
        assert updates == expected


class NakedCandidatesObjectUTest:
    def test__stringify(self) -> None:
        # Given
        transposed = True
        cells = [Cell(0, 1, (4, 5, 6, 7)), Cell(0, 2, (4, 5, 6)), Cell(0, 5, (4, 5, 6))]
        values = [4, 5, 6]
        obj = NakedCandidatesObject(transposed, cells, values)

        # When
        representation = str(obj)

        # Then
        assert representation == "[UPD] naked candidates [r1c2 r1c3 r1c6]@[5 6 7]\n"
        assert obj != 10

    def test__realign_not_transposed_should_be_self(self) -> None:
        # Given
        transposed = False
        cells = [Cell(0, 1, (4, 5, 6, 7)), Cell(0, 2, (4, 5, 6)), Cell(0, 5, (4, 5, 6))]
        values = [4, 5, 6]
        obj = NakedCandidatesObject(transposed, cells, values)

        # When
        result = obj.realign()

        # Then
        assert result == obj

    def test__realign_transposed_should_be_realigned(self) -> None:
        # Given
        transposed = True
        cells = [Cell(0, 1, (4, 5, 6, 7)), Cell(0, 2, (4, 5, 6)), Cell(0, 5, (4, 5, 6))]
        values = [4, 5, 6]
        obj = NakedCandidatesObject(transposed, cells, values)

        # When
        result = obj.realign()

        # Then
        assert result == NakedCandidatesObject(
            False, [cell.transpose() for cell in cells], values
        )
