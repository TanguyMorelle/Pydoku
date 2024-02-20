from src.adapters.solve_path_txt_handler import SolvePathTxtHandler
from src.domain.cell import Cell
from src.domain.solve_path import SolvePath
from src.domain.units import Units
from src.domain.updates import GridUpdate


class SolvePathTxtHandlerUTest:
    def test__save_should_write_empty_solve_path_to_file(self, tmp_path) -> None:
        # Given
        name = "test_solve_path_txt_handler_save"
        filename = tmp_path / name
        save_filename = tmp_path / (name + "_solve_path.txt")
        handler = SolvePathTxtHandler()
        solve_path = SolvePath(handler)

        # When
        handler.save(solve_path, filename)

        # Then
        assert save_filename.read_text() == "\n--END--"

    def test__save_should_write_solve_path_to_file(self, tmp_path) -> None:
        # Given
        name = "test_solve_path_txt_handler_save"
        filename = tmp_path / name
        save_filename = tmp_path / (name + "_solve_path.txt")
        handler = SolvePathTxtHandler()
        solve_path = SolvePath(handler)
        solve_path.path = [
            [
                GridUpdate(
                    unit=Units.ROW,
                    transposed=False,
                    cell=Cell(0, 1, (1,)),
                    possible_values_updates=[Cell(1, 1, (1,))],
                ),
                GridUpdate(
                    unit=Units.ROW,
                    transposed=True,
                    cell=Cell(5, 5, (2,)),
                    possible_values_updates=[
                        Cell(4, 3, (2,)),
                        Cell(4, 4, (2,)),
                    ],
                ),
            ],
            [
                GridUpdate(
                    unit=Units.ROW,
                    transposed=True,
                    cell=Cell(2, 2, (5,)),
                    possible_values_updates=[
                        Cell(0, 0, (5,)),
                        Cell(2, 6, (5,)),
                    ],
                )
            ],
        ]

        # When
        handler.save(solve_path, filename)

        # Then
        assert save_filename.read_text() == "\n".join(
            [
                "",
                "# STEP: 1",
                "  - [SET] unique option 2 [r1] @ r1c2",
                "    | removes 2 @ r2c2",
                "  - [SET] unique option 3 [r6] @ r6c6",
                "    | removes 3 @ r5c4",
                "    | removes 3 @ r5c5",
                "",
                "# STEP: 2",
                "  - [SET] unique option 6 [r3] @ r3c3",
                "    | removes 6 @ r1c1",
                "    | removes 6 @ r3c7",
                "",
                "--END--",
            ],
        )
