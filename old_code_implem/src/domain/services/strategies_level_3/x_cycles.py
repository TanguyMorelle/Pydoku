from operator import itemgetter
from typing import Any

from src.domain.models.cell import Cell
from src.domain.models.sudoku import Sudoku
from src.domain.models.unit import Unit
from src.domain.services.strategy import Strategy

Position = tuple[int, int]
Sequence = list[Position]
Mapping = dict[Position, list[Position]]
Link = tuple[Position, Position]


class XCycle:
    def __init__(self, sequence: Sequence) -> None:
        self.sequence = self._format_sequence(sequence)

    @staticmethod
    def _format_sequence(sequence: Sequence) -> Sequence:
        start = sorted(sequence, key=itemgetter(0, 1))[0]
        index = sequence.index(start)
        return sequence[index:] + sequence[:index]

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, XCycle):
            return self.sequence == other.sequence
        return False

    def __hash__(self) -> int:
        return hash(tuple(self.sequence))

    def __len__(self) -> int:
        return len(self.sequence)


class XCycles(Strategy):

    def __init__(self, sudoku: Sudoku) -> None:
        super().__init__(sudoku)

    def execute(self) -> None:
        for value in range(9):
            cells, strong_links, strong_link_mapping = self._get_cells_in_strong_links(value)
            visibility_mapping = self._get_visibility_mapping(cells)
            cycles = self._get_cycles(strong_links, visibility_mapping, strong_link_mapping)
            for cycle in cycles:
                if len(cycle) % 2 == 0:
                    self._rule_1(cycle, value)
                else:
                    self._rule_2(cycle, value, strong_link_mapping)

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

    def _get_cycles(
            self, strong_links: list[Link], visibility_mapping: Mapping, strong_links_mapping: Mapping
    ) -> list[XCycle]:
        cycles = []
        for link in strong_links:
            cycles += self._build_cycle([link[0], link[1]], strong_links, visibility_mapping, strong_links_mapping)
        return list(set(cycles))

    @staticmethod
    def _get_visibility_mapping(cells: list[Cell]) -> Mapping:
        cycle = {cell.position: [] for cell in cells}
        for i in range(len(cells)):
            p1 = cells[i].position
            for j in range(i + 1, len(cells)):
                p2 = cells[j].position
                if cells[i].check_visibility(cells[j]):
                    cycle[p1].append(p2)
                    cycle[p2].append(p1)
        return cycle

    def _build_cycle(
            self, sequence: Sequence, strong_links: list[Link], visibility_mapping: Mapping,
            strong_link_mapping: Mapping
    ) -> list[XCycle]:
        cycles = []
        # cells = set(visibility_mapping[sequence[-1]]) - set(strong_link_mapping[sequence[-1]])
        cells = set(visibility_mapping[sequence[-1]])
        for cell in cells:
            # case 1
            if cell == sequence[0] and len(sequence) > 3:
                cycles.append(XCycle(sequence))
            else:
                if cell not in sequence:
                    for node in strong_link_mapping[cell]:
                        # case 2
                        if node == sequence[0] and len(sequence) > 3:
                            cycles.append(XCycle(sequence + [cell]))
                        if node not in sequence:
                            cycles += self._build_cycle(
                                sequence + [cell, node], strong_links, visibility_mapping, strong_link_mapping
                            )
        return cycles

    def _rule_1(self, cycle: XCycle, value) -> None:
        cells = self.sudoku.get_possible_cells_for_value(value)
        positions = set(list(map(lambda cell: cell.position, cells))) - set(cycle.sequence)
        for position in positions:
            visibility = {0: 0, 1: 0}
            for i in range(len(cycle)):
                if has_visibility(cycle.sequence[i], position):
                    visibility[i % 2] += 1
            if visibility[0] > 0 and visibility[1] > 0:
                self.sudoku.possible_values_grid[position[0], position[1], value] = 0

    def _rule_2(self, cycle: XCycle, value: int, strong_link_mapping: Mapping) -> None:
        positions = list(set(range(9)) - {value})
        for i in range(len(cycle)):
            position = cycle.sequence[i]
            prev_pos = cycle.sequence[i - 1]
            next_pos = cycle.sequence[-1] if i == len(cycle) - 1 else cycle.sequence[i + 1]
            if prev_pos in strong_link_mapping[position] and next_pos in strong_link_mapping[position]:
                self.sudoku.possible_values_grid[position[0], position[1], positions] = 0


def has_visibility(position_1: Position, position_2: Position) -> bool:
    if position_1[0] == position_2[0]:
        return True
    if position_1[1] == position_2[1]:
        return True
    if position_1[0] // 3 == position_2[0] // 3 and position_1[1] // 3 == position_2[1] // 3:
        return True
    return False
