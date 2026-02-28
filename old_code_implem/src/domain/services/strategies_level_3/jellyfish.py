from src.domain.models.cell import Cell
from src.domain.models.sudoku import Sudoku
from src.domain.models.unit import Unit
from src.domain.services.strategy import Strategy

Quadruplet = tuple[list[int], list[int], list[Cell]]


class Jellyfish(Strategy):
    def __init__(self, sudoku: Sudoku):
        super().__init__(sudoku)

    def execute(self) -> None:
        for _ in range(2):
            for value in range(9):
                self._jellyfish(value)
            self.sudoku.transpose()

    def _jellyfish(self, value: int) -> None:
        cells_on_valid_line = []
        for i in range(2, 5):
            cells_on_valid_line += self.sudoku.get_n_optioned_unit(value, Unit.LINE, i)
        quadruplets = self._get_quadruplets(cells_on_valid_line)
        for line, columns, cells in quadruplets:
            cells_to_update = set([(m, n) for m in range(9) for n in columns]) - set([cell.position for cell in cells])
            for cell in cells_to_update:
                self.sudoku.possible_values_grid[cell[0], cell[1], value] = 0

    @staticmethod
    def _get_quadruplets(valid_lines: list[list[Cell]]) -> list[Quadruplet]:
        quadruplets = []
        for i in range(len(valid_lines)):
            for j in range(i + 1, len(valid_lines)):
                for k in range(j + 1, len(valid_lines)):
                    for l in range(k + 1, len(valid_lines)):
                        cells: list[Cell] = []
                        for idx in [i, j, k, l]:
                            cells += valid_lines[idx]
                        lines = list(set(map(lambda cell: cell.line, cells)))
                        columns = list(set(map(lambda cell: cell.column, cells)))
                        if len(set(columns)) == 4:
                            quadruplets.append((lines, columns, cells))
        return quadruplets
