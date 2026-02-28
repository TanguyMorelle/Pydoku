from src.domain.models.cell import Cell
from src.domain.models.sudoku import Sudoku
from src.domain.services.strategy import Strategy

Position = tuple[int, int]
Mapping = dict[Position, list[Position]]
Sequence = list[Position]


class XYChain:
    def __init__(self, sequence: Sequence, values: list[tuple[int, int]]) -> None:
        self.sequence = sequence
        self.values = values

    @property
    def get_start_end_visible_cells(self) -> list[Position]:
        start, end = self.sequence[0], self.sequence[-1]
        if len(self.sequence) < 3:
            return []
        visibility_start, visibility_end = get_visibility(start), get_visibility(end)
        bi_visible_cells = []
        for position in visibility_start:
            if position in visibility_end:
                bi_visible_cells.append(position)
        return list(set(bi_visible_cells) - set(self.sequence))

    @property
    def common_start_end_values(self) -> bool:
        if len(self.sequence) < 3:
            return False
        return self.values[0][0] == self.values[-1][-1]


class XYChains(Strategy):
    def __init__(self, sudoku: Sudoku) -> None:
        super().__init__(sudoku)

    def execute(self) -> None:
        cells = self.sudoku.get_n_valued_cells(self.sudoku.possible_values_grid, 2)
        visibility_mapping = self._get_visibility_mapping(cells)
        value_mapping = {cell.position: cell.values for cell in cells}
        for cell in cells:
            chains = []
            values = value_mapping[cell.position]
            chains += self._build_chains([cell.position], [values], visibility_mapping, value_mapping)
            chains += self._build_chains([cell.position], [(values[1], values[0])], visibility_mapping, value_mapping)
            for chain in chains:
                self._update(chain)

    def _update(self, chain: XYChain) -> None:
        if chain.common_start_end_values:
            positions = chain.get_start_end_visible_cells
            value = chain.values[0][0]
            for position in positions:
                if self.sudoku.possible_values_grid[position[0], position[1], value] == 1:
                    self.sudoku.possible_values_grid[position[0], position[1], value] = 0

    def _build_chains(
            self, sequence: Sequence, values: list[tuple[int, int]], visibility_mapping: Mapping,
            value_mapping: dict[Position, tuple[int, int]]
    ) -> list[XYChain]:
        chains = [XYChain(sequence, values)]
        cells = set(visibility_mapping[sequence[-1]]) - set(sequence)
        for cell in cells:
            value_1, value_2 = value_mapping[cell]
            if value_1 == values[-1][-1]:
                chains += self._build_chains(sequence + [cell], values + [(value_1, value_2)], visibility_mapping,
                                             value_mapping)
            if value_2 == values[-1][-1]:
                chains += self._build_chains(sequence + [cell], values + [(value_2, value_1)], visibility_mapping,
                                             value_mapping)
        return chains

    @staticmethod
    def _get_visibility_mapping(cells: list[Cell]) -> Mapping:
        mapping = {cell.position: [] for cell in cells}
        for i in range(len(cells)):
            p1 = cells[i].position
            for j in range(i + 1, len(cells)):
                p2 = cells[j].position
                if cells[i].check_visibility(cells[j]):
                    mapping[p1].append(p2)
                    mapping[p2].append(p1)
        return mapping


def get_visibility(position: Position) -> list[Position]:
    positions = []
    u, v = 3 * (position[0] // 3), 3 * (position[1] // 3)
    positions += [(i, position[1]) for i in range(9)]
    positions += [(position[0], j) for j in range(9)]
    positions += [(i, j) for i in range(u, u + 3) for j in range(v, v + 3)]
    return list(set(positions) - {position})
