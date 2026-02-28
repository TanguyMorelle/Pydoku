from src.domain.models.cell import Cell
from src.domain.models.sudoku import Sudoku
from src.domain.services.strategy import Strategy

Position = tuple[int, int]


class YWing(Strategy):
    def __init__(self, sudoku: Sudoku) -> None:
        super().__init__(sudoku)

    def execute(self) -> None:
        cells = self.sudoku.get_n_valued_cells(self.sudoku.possible_values_grid, 2)
        for cell in cells:
            self._y_wing(cells, cell)

    def _y_wing(self, cells: list[Cell], pivot_cell: Cell) -> None:
        line_cells = list(filter(lambda cell: self._filter_line(pivot_cell, cell), cells))
        column_cells = list(filter(lambda cell: self._filter_column(pivot_cell, cell), cells))
        block_cells = list(filter(lambda cell: self._filter_block(pivot_cell, cell), cells))
        for cell_line in line_cells:
            for cell_column in column_cells:
                self._update(cell_line, cell_column, pivot_cell)
        for cell_block in block_cells:
            for cell_column in column_cells:
                self._update(cell_block, cell_column, pivot_cell)
            for cell_line in line_cells:
                self._update(cell_block, cell_line, pivot_cell)

    def _update(self, cell_1: Cell, cell_2: Cell, pivot_cell: Cell) -> None:
        value_1 = (set(cell_1.values) - set(pivot_cell.values)).pop()
        value_2 = (set(cell_2.values) - set(pivot_cell.values)).pop()
        if value_1 == value_2 and cell_1.values != cell_2.values:
            positions = self._get_bi_visible_cells(cell_1, cell_2) - {pivot_cell.position}
            for position in positions:
                self.sudoku.possible_values_grid[position[0], position[1], value_1] = 0

    @staticmethod
    def _filter_line(pivot_cell: Cell, cell: Cell) -> bool:
        columns = list(set(range(9)) - set([3 * (pivot_cell.column // 3) + j for j in range(3)]))
        return (
                cell.line == pivot_cell.line and
                cell.column in columns and
                len(set(cell.values) - set(pivot_cell.values)) == 1
        )

    @staticmethod
    def _filter_column(pivot_cell: Cell, cell: Cell) -> bool:
        lines = list(set(range(9)) - set([3 * (pivot_cell.line // 3) + i for i in range(3)]))
        return (
                cell.line in lines and
                cell.column == pivot_cell.column and
                len(set(cell.values) - set(pivot_cell.values)) == 1
        )

    @staticmethod
    def _filter_block(pivot_cell: Cell, cell: Cell) -> bool:
        lines = [3 * (pivot_cell.line // 3) + i for i in range(3)]
        columns = [3 * (pivot_cell.column // 3) + j for j in range(3)]
        return (
                cell.line in lines and
                cell.column in columns and
                len(set(cell.values) - set(pivot_cell.values)) == 1
        )

    @staticmethod
    def _get_bi_visible_cells(cell_1: Cell, cell_2: Cell) -> set[Position]:
        visible_from_cell_1, visible_from_cell_2 = [], []
        u, v = 3 * (cell_1.line // 3), 3 * (cell_1.column // 3)
        visible_from_cell_1 += [(i, cell_1.column) for i in range(9)]
        visible_from_cell_1 += [(cell_1.line, j) for j in range(9)]
        visible_from_cell_1 += [(i, j) for i in range(u, u + 3) for j in range(v, v + 3)]
        visible_from_cell_1 = set(visible_from_cell_1) - {cell_1.position}

        u, v = 3 * (cell_2.line // 3), 3 * (cell_2.column // 3)
        visible_from_cell_2 += [(i, cell_2.column) for i in range(9)]
        visible_from_cell_2 += [(cell_2.line, j) for j in range(9)]
        visible_from_cell_2 += [(i, j) for i in range(u, u + 3) for j in range(v, v + 3)]
        visible_from_cell_2 = set(visible_from_cell_2) - {cell_2.position}

        return visible_from_cell_1.intersection(visible_from_cell_2)
