from src.domain.models.cell import Cell
from src.domain.models.sudoku import Sudoku
from src.domain.models.unit import Unit
from src.domain.services.strategy import Strategy


class Fish:
    def __init__(self, cells: list[Cell], level: int) -> None:
        if level < 2 or level > 8:
            raise Exception
        self.cells = cells
        self.level = level
        self.lines = list(set(map(lambda cell: cell.line, self.cells)))
        self.columns = list(set(map(lambda cell: cell.column, self.cells)))

    @property
    def is_valid(self) -> bool:
        return len(set(self.columns)) == self.level


class GeneralizedFish(Strategy):
    def __init__(self, sudoku: Sudoku, level: int) -> None:
        super().__init__(sudoku)
        self.level = level

    def execute(self) -> None:
        for _ in range(2):
            for value in range(9):
                self._fish(value)
            self.sudoku.transpose()

    def _fish(self, value: int) -> None:
        cells_on_valid_line = []
        for i in range(2, self.level + 1):
            cells_on_valid_line += self.sudoku.get_n_optioned_unit(value, Unit.LINE, i)
        fishes = self._get_fish(self.level, [], cells_on_valid_line)
        for fish in fishes:
            updated = self._update(fish, value)
            if updated:
                return

    def _update(self, fish: Fish, value: int) -> bool:
        updated = False
        lines, columns, cells = fish.lines, fish.columns, fish.cells
        cells_to_update = set([(m, n) for m in range(9) for n in columns]) - set([cell.position for cell in cells])
        for cell in cells_to_update:
            if self.sudoku.possible_values_grid[cell[0], cell[1], value] == 1:
                self.sudoku.possible_values_grid[cell[0], cell[1], value] = 0
                updated = True
        return updated

    def _get_fish(self, level: int, indexes: list[int], valid_lines: list[list[Cell]]) -> list[Fish]:
        valid_fishes = []
        if level == 0:
            cells: list[Cell] = []
            for idx in indexes:
                cells += valid_lines[idx]
            fish = Fish(cells, self.level)
            if fish.is_valid:
                valid_fishes.append(fish)
        else:
            min_index = 0 if len(indexes) == 0 else indexes[-1] + 1
            for i in range(min_index + 1, len(valid_lines)):
                valid_fishes += self._get_fish(level - 1, indexes + [i], valid_lines)
        return valid_fishes
