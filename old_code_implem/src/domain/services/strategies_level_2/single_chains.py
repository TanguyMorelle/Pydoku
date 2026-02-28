from collections import namedtuple

import numpy as np

from src.domain.models.cell import Cell
from src.domain.models.sudoku import Sudoku
from src.domain.models.unit import Unit
from src.domain.services.strategy import Strategy

Position = tuple[int, int]
Mapping = dict[Position, list[Position]]
ColoredNode = namedtuple('ColoredNode', ['color', 'links'])
ColoredMapping = dict[Position, ColoredNode]


class SingleChains(Strategy):
    def __init__(self, sudoku: Sudoku) -> None:
        super().__init__(sudoku)

    def execute(self) -> None:
        for value in range(9):
            self._single_chains(value)

    def _single_chains(self, value: int, rule_2: bool = True, rule_4: bool = True) -> None:
        cycles = self._get_cycles(value)
        for cycle in cycles:
            colored_cycle = self._get_colored_cycle(cycle)
            if rule_2:
                self._rule_2(colored_cycle, value)
            if rule_4:
                self._rule_4(colored_cycle, value)

    def _rule_2(self, cycle: ColoredMapping, value: int) -> None:
        nodes = list(cycle.keys())
        for line in range(9):
            visible_nodes = list(filter(lambda node: node[0] == line, nodes))
            self._check_invalid_configurations(cycle, visible_nodes, value)
        for column in range(9):
            visible_nodes = list(filter(lambda node: node[1] == column, nodes))
            self._check_invalid_configurations(cycle, visible_nodes, value)
        for y in range(3):
            for x in range(3):
                visible_nodes = list(filter(lambda node: node[0] // 3 == y and node[1] // 3 == x, nodes))
                self._check_invalid_configurations(cycle, visible_nodes, value)

    def _check_invalid_configurations(self, cycle: ColoredMapping, visible_nodes: list[Position], value) -> None:
        visible_colors = {True: 0, False: 0}
        for node in visible_nodes:
            visible_colors[cycle[node].color] += 1
        for color in visible_colors:
            if visible_colors[color] == 2:
                for position, colored_node in cycle.items():
                    if colored_node.color == color:
                        self.sudoku.possible_values_grid[position[0], position[1], value] = 0

    def _rule_4(self, cycle: ColoredMapping, value: int) -> None:
        y_pos, x_pos = np.where(self.sudoku.possible_values_grid[:, :, value] == 1)
        cells = [Cell(i, j, (value,)) for i, j in set(zip(y_pos, x_pos)) - set(cycle.keys())]
        for cell in cells:
            visible_colors = []
            for node, coloredNode in cycle.items():
                if cell.check_visibility(node):
                    visible_colors.append(coloredNode.color)
            if len(set(visible_colors)) == 2:
                self.sudoku.possible_values_grid[cell.line, cell.column, value] = 0

    def _get_cycles(self, value: int) -> list[Mapping]:
        visibility_mapping = self._get_cycle_map(value)
        cycle_groups = []
        elements_without_group = set(visibility_mapping.keys())
        while len(elements_without_group) > 0:
            element = elements_without_group.pop()
            cycle = self._get_cycle(element, visibility_mapping)
            cycle_groups.append(cycle)
            elements_without_group -= set(cycle.keys())
        return cycle_groups

    def _get_cycle_map(self, value: int) -> Mapping:
        line_cells = self.sudoku.get_n_optioned_unit(value, Unit.LINE, 2)
        column_cells = self.sudoku.get_n_optioned_unit(value, Unit.COLUMN, 2)
        block_cells = self.sudoku.get_n_optioned_unit(value, Unit.BLOCK, 2)
        cells = line_cells + column_cells + block_cells
        visibility_mapping: Mapping = {}
        for cell_1, cell_2 in cells:
            cell_1_links = visibility_mapping[cell_1.position] if cell_1.position in visibility_mapping.keys() else []
            cell_2_links = visibility_mapping[cell_2.position] if cell_2.position in visibility_mapping.keys() else []
            if cell_2.position not in cell_1_links:
                cell_1_links.append(cell_2.position)
                visibility_mapping[cell_1.position] = cell_1_links
            if cell_1.position not in cell_2_links:
                cell_2_links.append(cell_1.position)
                visibility_mapping[cell_2.position] = cell_2_links
        return visibility_mapping

    @staticmethod
    def _get_cycle(position: Position, visibility_mapping: Mapping) -> Mapping:
        length = 0
        cycle = {position: visibility_mapping[position]}
        while len(cycle.keys()) > length:
            length = len(cycle.keys())
            links = []
            for values in cycle.values():
                links += values
            new_values = set(links) - set(cycle.keys())
            for value in new_values:
                cycle[value] = visibility_mapping[value]
        return cycle

    @staticmethod
    def _get_colored_cycle(visibility_mapping: Mapping) -> ColoredMapping:
        colored_mapping = {}
        nodes = list(visibility_mapping.keys())
        colored_mapping[nodes[0]] = ColoredNode(True, visibility_mapping[nodes[0]])
        while len(colored_mapping.keys()) < len(nodes):
            cells_to_check = list(colored_mapping.keys())
            for element in cells_to_check:
                for link in colored_mapping[element].links:
                    if link not in colored_mapping.keys():
                        colored_mapping[link] = ColoredNode(not colored_mapping[element].color, visibility_mapping[link])
        return colored_mapping
