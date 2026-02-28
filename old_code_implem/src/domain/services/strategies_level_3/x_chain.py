from typing import Any

from src.domain.models.cell import Cell
from src.domain.models.sudoku import Sudoku
from src.domain.models.unit import Unit
from src.domain.services.strategy import Strategy

Position = tuple[int, int]
Sequence = list[Position]
Mapping = dict[Position, list[Position]]
Link = tuple[Position, Position]


class XChain:
    def __init__(self, sequence: list[Position]) -> None:
        self.sequence = sequence

    @property
    def missing_links_to_cycle(self) -> list[Position]:
        start, end = self.sequence[0], self.sequence[-1]
        if len(self) < 4 or has_visibility(start, end):
            return []
        positions = []
        if start[0] // 3 != end[0] // 3 and start[1] // 3 == end[1] // 3:
            x1, x2 = start[1], end[1]
            u, v = 3 * (start[0] // 3), 3 * (end[0] // 3)
            positions = [(i, x1) for i in range(v, v + 3)] + [(i, x2) for i in range(u, u + 3)]
        if start[0] // 3 != end[0] // 3 and start[1] // 3 != end[1] // 3:
            positions = [(start[0], end[1]), (end[0], start[1])]
        if start[0] // 3 == end[0] // 3 and start[1] // 3 != end[1] // 3:
            y1, y2 = start[0], end[0]
            u, v = 3 * (start[1] // 3), 3 * (end[1] // 3)
            positions = [(y1, j) for j in range(v, v + 3)] + [(y2, j) for j in range(u, u + 3)]
        if start[0] // 3 != end[0] // 3 and start[1] // 3 == end[1] // 3:
            x1, x2 = start[1], end[1]
            u, v = 3 * (start[0] // 3), 3 * (end[0] // 3)
            positions = [(i, x1) for i in range(v, v + 3)] + [(i, x2) for i in range(u, u + 3)]
        return positions

    def __len__(self) -> int:
        return len(self.sequence)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, XChain):
            return self.sequence == other.sequence
        return False


class XChains(Strategy):
    def __init__(self, sudoku: Sudoku) -> None:
        super().__init__(sudoku)

    def execute(self) -> None:
        for value in range(9):
            self._x_chain(value)

    def _x_chain(self, value: int) -> None:
        cells, strong_links, strong_link_mapping = self._get_cells_in_strong_links(value)
        cell_visibility_mapping = self._get_cell_visibility_mapping(cells)
        chains = self._get_chains(cell_visibility_mapping, strong_link_mapping)
        self._update(value, chains)

    def _get_cells_in_strong_links(self, value: int) -> tuple[list[Cell], list[Link], Mapping]:
        lines = self.sudoku.get_n_optioned_unit(value, Unit.LINE, 2)
        columns = self.sudoku.get_n_optioned_unit(value, Unit.COLUMN, 2)
        blocks = self.sudoku.get_n_optioned_unit(value, Unit.BLOCK, 2)
        cells_ = []
        strong_links = list(map(lambda link_: (link_[0].position, link_[1].position), lines + columns + blocks))
        for couple in lines + columns + blocks:
            cells_.append(couple[0])
            cells_.append(couple[1])
        cells = list(set(cells_))
        strong_link_mapping: Mapping = {}
        for link in strong_links:
            p0, p1 = link[0], link[1]
            link_cell_0 = strong_link_mapping[p0] if p0 in strong_link_mapping.keys() else []
            link_cell_1 = strong_link_mapping[p1] if p1 in strong_link_mapping.keys() else []
            strong_link_mapping[p0] = list(set(link_cell_0 + [p1]))
            strong_link_mapping[p1] = list(set(link_cell_1 + [p0]))
        return cells, strong_links, strong_link_mapping

    @staticmethod
    def _get_cell_visibility_mapping(cells: list[Cell]) -> Mapping:
        cycle = {cell.position: [] for cell in cells}
        for i in range(len(cells)):
            p1 = cells[i].position
            for j in range(i + 1, len(cells)):
                p2 = cells[j].position
                if cells[i].check_visibility(cells[j]):
                    cycle[p1].append(p2)
                    cycle[p2].append(p1)
        return cycle

    def _get_chains(self, visibility_mapping: Mapping, strong_link_mapping: Mapping) -> list[XChain]:
        chains: list[XChain] = []
        for cell in strong_link_mapping.keys():
            for node in strong_link_mapping[cell]:
                chains += self._build_chains([cell, node], visibility_mapping, strong_link_mapping)
        return chains

    def _build_chains(self, sequence: Sequence, cycle_mapping: Mapping, strong_link_mapping: Mapping) -> list[XChain]:
        chains = [XChain(sequence)] if len(sequence) > 3 else []
        # cells = set(cycle_mapping[sequence[-1]]) - set(strong_link_mapping[sequence[-1]])
        cells = set(cycle_mapping[sequence[-1]])
        for cell in cells:
            if cell not in sequence:
                for node in strong_link_mapping[cell]:
                    if node not in sequence:
                        chains += self._build_chains(sequence + [cell, node], cycle_mapping, strong_link_mapping)
        return chains

    def _update(self, value: int, chains: list[XChain]) -> None:
        for chain in chains:
            for position in chain.missing_links_to_cycle:
                if position not in chain.sequence:
                    self.sudoku.possible_values_grid[position[0], position[1], value] = 0


def has_visibility(position_1: Position, position_2: Position) -> bool:
    if position_1[0] == position_2[0]:
        return True
    if position_1[1] == position_2[1]:
        return True
    if position_1[0] // 3 == position_2[0] // 3 and position_1[1] // 3 == position_2[1] // 3:
        return True
    return False
