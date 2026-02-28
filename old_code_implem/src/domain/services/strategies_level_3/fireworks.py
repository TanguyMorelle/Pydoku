from typing import Optional

import numpy as np

from src.domain.models.sudoku import Sudoku
from src.domain.services.strategy import Strategy

Position = tuple[int, int]


class Firework:
    def __init__(self, value: int, positions: list[Position], intersections: list[Position], isolated_cell: Optional[Position] = None) -> None:
        self.value = value
        self.positions = positions
        self.intersections = intersections
        self.isolated_cell = isolated_cell


class Fireworks(Strategy):
    def __init__(self, sudoku: Sudoku) -> None:
        super().__init__(sudoku)

    def execute(self) -> None:
        # setup
        fireworks_line = {}
        fireworks_column = {}
        for i in range(9):
            fireworks_line[i] = self.firework_cells_line(i)
        for j in range(9):
            fireworks_column[j] = self.firework_cells_line(j)
        # do stuff
        for i in range(9):
            for j in range(9):
                pass

    def firework_cells_line(self, i: int) -> dict[int, list[Firework]]:
        fireworks = {value: [] for value in range(9)}
        missing_values = self.sudoku.get_missing_values(self.sudoku[i, :])
        for value in missing_values:
            y_pos, x_pos = np.where(self.sudoku.possible_values_grid[i, :, value] == 1)
            block_count = {}
            for j in x_pos:
                if j // 3 in block_count.keys():
                    block_count[j // 3].append((i, j))
                else:
                    block_count[j // 3] = [(i, j)]
            positions = list(zip(y_pos, x_pos))
            if len(block_count) == 2:
                if len(block_count[0]) == 1:
                    fireworks[value].append(Firework(value, positions, block_count[1], block_count[0][0]))
                if len(block_count[1]) == 1:
                    fireworks[value].append(Firework(value, positions, block_count[0], block_count[1][0]))
            if len(block_count) == 1:
                fireworks[value].append(Firework(value, positions, block_count[0]))
        return fireworks

    def firework_cells_column(self, j: int) -> dict[int, list[Firework]]:
        fireworks = {value: [] for value in range(9)}
        missing_values = self.sudoku.get_missing_values(self.sudoku[:, j])
        for value in missing_values:
            y_pos, x_pos = np.where(self.sudoku.possible_values_grid[:, j, value] == 1)
            block_count = {}
            for i in y_pos:
                if i // 3 in block_count.keys():
                    block_count[i // 3].append((i, j))
                else:
                    block_count[i // 3] = [(i, j)]
            positions = list(zip(y_pos, x_pos))
            if len(block_count) == 2:
                if len(block_count[0]) == 1:
                    fireworks[value].append(Firework(value, positions, block_count[1], block_count[0][0]))
                if len(block_count[1]) == 1:
                    fireworks[value].append(Firework(value, positions, block_count[0], block_count[1][0]))
            if len(block_count) == 1:
                fireworks[value].append(Firework(value, positions, block_count[0]))
        return fireworks

    def test(self, i: int, j: int, f1: dict[int, list[Firework]], f2: dict[int, list[Firework]]):
        valid_fireworks_line = {}
        valid_fireworks_column = {}
        for value in range(9):
            fireworks_line: list[Firework] = list(filter(lambda element: (i, j) in element.intersections, f1[value]))
            if len(fireworks_line) > 0:
                position = fireworks_line[0].isolated_cell
                if position in valid_fireworks_line.keys():
                    valid_fireworks_line[position].append(fireworks_line[0])
                else:
                    valid_fireworks_line[position].append(fireworks_line[0])
            fireworks_column: list[Firework] = list(filter(lambda element: (i, j) in element.intersections, f2[value]))
            if len(fireworks_column) > 0:
                position = fireworks_column[0].isolated_cell
                if position in valid_fireworks_column.keys():
                    valid_fireworks_column[position].append(fireworks_column[0])
                else:
                    valid_fireworks_column[position].append(fireworks_column[0])
        if len(valid_fireworks_line.keys()) >= 3:
            line_mapping = {}
            line_values = {}

    def dual_firework_y_wing(self):
        pass

    def dual_firework_l_wing(self):
        pass

    def dual_firework_alp(self):
        pass

    def firework_triple(self):
        pass

    def firework_quadruple(self):
        pass

    def firework_exocet(self):
        pass

    def kraken_firework(self):
        pass