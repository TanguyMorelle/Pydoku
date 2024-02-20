import numpy as np

from src.domain.cell import Cell
from src.domain.strategies.strategy import Strategy
from src.domain.sudoku import Sudoku
from src.domain.units import Units
from src.domain.updates import GridUpdate, Update


class Unicity(Strategy):
    def __init__(self, sudoku: Sudoku) -> None:
        super().__init__(sudoku)
        self.updated_cells: list[Cell] = []
        self.grid_updates: list[Update] = []

    def execute(self) -> list[Update]:
        for _ in range(2):
            for row in range(9):
                for column in range(9):
                    self._unicity_in_cell(row, column)
                self._unicity_in_row(row)
            self.sudoku.transpose()
        for block in range(9):
            self._unicity_in_block(block)
        return self.grid_updates

    def _unicity_in_cell(self, row: int, column: int) -> None:
        (values,) = np.where(self.sudoku.possible_values_grid[row, column] == 1)
        if len(values) == 1:
            self.update_grid_updates(Units.CELL, row, column, values[0])

    def _unicity_in_row(self, row: int) -> None:
        missing_values = self.sudoku.get_missing_values(Units.ROW, row)
        for value in missing_values:
            (columns,) = np.where(
                self.sudoku.possible_values_grid.get_row(row, value) == 1
            )
            if len(columns) == 1:
                self.update_grid_updates(Units.ROW, row, columns[0], value)

    def _unicity_in_block(self, block: int) -> None:
        u, v = divmod(block, 3)
        missing_values = self.sudoku.get_missing_values(Units.BLOCK, block)
        for value in missing_values:
            rows, columns = np.where(
                self.sudoku.possible_values_grid.get_block(block, value) == 1
            )
            if len(rows) == 1:
                self.update_grid_updates(
                    Units.BLOCK, 3 * u + rows[0], 3 * v + columns[0], value
                )

    def update_grid_updates(
        self, unit: Units, row: int, column: int, value: int
    ) -> None:
        cell_to_update = Cell(row, column, (value,))
        update = GridUpdate(
            unit=unit,
            cell=cell_to_update,
            transposed=self.sudoku.transposed,
            possible_values_updates=self._get_visible_cells_to_update(cell_to_update),
        ).realign()
        if update.cell not in self.updated_cells:
            self.updated_cells.append(update.cell)
            self.grid_updates.append(update)

    def _get_visible_cells_to_update(self, cell: Cell) -> list[Cell]:
        value = cell.values[0]
        cells = []
        for position in cell.visibility:
            if self.sudoku.possible_values_grid[*position, value] == 1:
                cells.append(Cell(*position, (value,)))
        return cells
