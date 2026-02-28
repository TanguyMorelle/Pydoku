import numpy as np

from src.domain.models.sudoku import Sudoku
from src.domain.services.strategy import Strategy

Position: tuple[int, int]


class UniqueRectangles(Strategy):
    def __init__(self, sudoku: Sudoku) -> None:
        super().__init__(sudoku)

    def execute(self) -> None:
        for value_1 in range(9):
            for value_2 in range(9):
                bi_valued_cells = self._get_bi_valued_cells(value_1, value_2)
                tri_valued_cells = self._get_tri_valued_cells(value_1, value_2)
                self.class_1(value_1, value_2, bi_valued_cells)
                self.class_2(bi_valued_cells, tri_valued_cells)

    def class_1(self, value_1: int, value_2: int, bi_valued_cells: list[Position]) -> None:
        edges = self._get_unfilled_edges(bi_valued_cells)
        for edge in edges:
            self.sudoku.possible_values_grid[edge[0], edge[1], [value_1, value_2]] = 0

    @staticmethod
    def _get_unfilled_edges(positions: list[Position]) -> list[Position]:
        edges = []
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                for k in range(j + 1, len(positions)):
                    y1, x1 = positions[i]
                    y2, x2 = positions[j]
                    y3, x3 = positions[k]
                    has_same_unit = len({y1 // 3, y2 // 3, y3 // 3}) == 1 or len({x1 // 3, x2 // 3, x3 // 3}) == 1
                    if len({y1, y2, y3}) == 2 and len({x1, x2, x3}) == 2 and has_same_unit:
                        edges = [(i, j) for i in {y1, y2, y3} for j in {x1, x2, x3}]
                        missing_edge = (set(edges) - {positions[i], positions[j], positions[k]}).pop()
                        edges.append(missing_edge)
        return edges

    def class_2(
        self, bi_valued_cells: list[Position], tri_valued_cells: dict[int, Position]
    ) -> None:
        value_cells = self._get_class_2_rectangle(bi_valued_cells, tri_valued_cells)
        for value, pos_1, pos_2 in value_cells:
            positions_1 = self.sudoku.get_visibility(pos_1)
            positions_2 = self.sudoku.get_visibility(pos_2)
            positions = set(positions_1).intersection(set(positions_2))
            for position in positions:
                self.sudoku.possible_values_grid[position[0], position[1], value] = 0

    @staticmethod
    def _get_class_2_rectangle(
        bi_valued_cells: list[Position], tri_valued_cells: dict[int, Position]
    ) -> list[tuple[int, Position, Position]]:
        rectangles_tri_valued_cells: list[tuple[int, Position, Position]] = []
        for value in tri_valued_cells.keys():
            tri_cells = tri_valued_cells[value]
            for i in range(len(bi_valued_cells)):
                for j in range(i + 1, len(bi_valued_cells)):
                    for u in range(len(tri_cells)):
                        for v in range(u + 1, len(tri_cells)):
                            y1, x1 = bi_valued_cells[i]
                            y2, x2 = bi_valued_cells[j]
                            y3, x3 = tri_cells[u]
                            y4, x4 = tri_cells[v]
                            has_same_line_block = len({y1 // 3, y2 // 3, y3 // 3, y4 // 4}) == 1
                            has_same_column_block = len({x1 // 3, x2 // 3, x3 // 3, x4 // 3}) == 1
                            has_same_unit = has_same_line_block or has_same_column_block
                            if len({y1, y2, y3, y4}) == 2 and len({x1, x2, x3, x4}) == 2 and has_same_unit:
                                rectangles_tri_valued_cells.append((value, tri_cells[u], tri_cells[v]))
        return rectangles_tri_valued_cells

    def class_3(self):
        pass

    def _get_bi_valued_cells(self, value_1: int, value_2: int) -> list[Position]:
        values = np.zeros(9)
        values[[value_1, value_2]] = 1
        y_pos, x_pos = np.where(self.sudoku.possible_values_grid[:, :] == values)
        positions: list[Position] = list(zip(y_pos, x_pos))
        return positions

    def _get_tri_valued_cells(self, value_1: int, value_2: int) -> dict[int, list[Position]]:
        y_pos, x_pos, _ = np.where(np.sum(self.sudoku.possible_values_grid[:, :, [value_1, value_2]], axis=2) == 2)
        bi_value_cells: list[Position] = list(zip(y_pos, x_pos))
        y_pos, x_pos = np.where(np.sum(self.sudoku.possible_values_grid[:, :, :], axis=2) == 3)
        tri_value_cells: list[Position] = list(zip(y_pos, x_pos))
        valid_cells = set(bi_value_cells).intersection(set(tri_value_cells))
        to_return = {}
        for position in valid_cells:
            values = self.sudoku.get_values_for_position(position)
            additional_value = (set(values) - {value_1, value_2}).pop()
            if additional_value in to_return.keys():
                to_return[additional_value].append(position)
            else:
                to_return[additional_value] = [position]
        return to_return
