from src.domain.models.cell import Cell
from src.domain.models.sudoku import Sudoku
from src.domain.services.strategy import Strategy

Position = tuple[int, int]


class XYZWing(Strategy):
    def __init__(self, sudoku: Sudoku) -> None:
        super().__init__(sudoku)

    def execute(self) -> None:
        for _ in range(2):
            pivot_cells = self.sudoku.get_n_valued_cells(self.sudoku.possible_values_grid, 3)
            cells = self.sudoku.get_n_valued_cells(self.sudoku.possible_values_grid, 2)
            for cell in pivot_cells:
                self._xyz_wing(cells, cell)
            self.sudoku.transpose()

    def _xyz_wing(self, cells: list[Cell], pivot_cell: Cell) -> None:
        line_cells = list(filter(lambda cell: self._filter_line(pivot_cell, cell), cells))
        block_cells = list(filter(lambda cell: self._filter_block(pivot_cell, cell), cells))
        for cell_block in block_cells:
            for cell_line in line_cells:
                self._update(cell_block, cell_line, pivot_cell)

    def _update(self, cell_block: Cell, cell_line: Cell, pivot_cell: Cell) -> None:
        diff_1 = (set(pivot_cell.values) - set(cell_block.values)).pop()
        diff_2 = (set(pivot_cell.values) - set(cell_line.values)).pop()
        if diff_1 != diff_2 and cell_line.values != cell_block.values:
            value = (set(pivot_cell.values) - {diff_1, diff_2}).pop()
            v = 3 * (pivot_cell.column // 3)
            positions = set([(cell_line.line, j) for j in range(v, v + 3)]) - {cell_block.position, pivot_cell.position}
            for position in positions:
                self.sudoku.possible_values_grid[position[0], position[1], value] = 0

    @staticmethod
    def _filter_line(pivot_cell: Cell, cell: Cell) -> bool:
        columns = list(set(range(9)) - set([3 * (pivot_cell.column // 3) + j for j in range(3)]))
        return (
                cell.line == pivot_cell.line and
                cell.column in columns and
                len(set(pivot_cell.values) - set(cell.values)) == 1
        )

    @staticmethod
    def _filter_block(pivot_cell: Cell, cell: Cell) -> bool:
        lines = [3 * (pivot_cell.line // 3) + i for i in range(3)]
        columns = [3 * (pivot_cell.column // 3) + j for j in range(3)]
        return (
                cell.line in lines and
                cell.column in columns and
                len(set(pivot_cell.values) - set(cell.values)) == 1
        )
