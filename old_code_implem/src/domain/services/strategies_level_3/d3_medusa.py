import numpy as np

from src.domain.models.cell import Cell
from src.domain.models.sudoku import Sudoku
from src.domain.models.unit import Unit
from src.domain.services.strategy import Strategy

Position = tuple[int, int]
Mapping = dict[Position, list[Cell]]
Link = list[Cell, Cell]


class Node:
    def __init__(self, cell: Cell, color: int) -> None:
        self.cell = cell
        self.color = color

    @property
    def position(self) -> Position:
        return self.cell.position

    @property
    def value(self) -> int:
        return self.cell.values[0]

    @property
    def line(self) -> int:
        return self.cell.line

    @property
    def column(self) -> int:
        return self.cell.column

    def __eq__(self, other) -> bool:
        if isinstance(other, Node):
            return self.color == other.color and self.cell == other.cell
        return False

class Medusa:
    def __init__(self) -> None:
        self.cells = []
        self.nodes: list[Node] = []
        self.positions = []

    def add_node(self, node: Node) -> None:
        if node.cell not in self.cells:
            self.cells.append(node.cell)
            self.nodes.append(node)
            if node.position not in self.positions:
                self.positions.append(node.position)

    def __eq__(self, other) -> bool:
        if isinstance(other, Medusa):
            return self.nodes == other.nodes
        return False


class D3Medusa(Strategy):
    def __init__(self, sudoku: Sudoku) -> None:
        super().__init__(sudoku)

    def execute(self) -> None:
        medusas = self._get_medusas()
        for medusa in medusas:
            self._rule_1(medusa)
            self._rule_2(medusa)
            self._rule_3(medusa)
            self._rule_4(medusa)
            self._rule_5(medusa)
            self._rule_6(medusa)

    def get_strong_links(self) -> list[Link]:
        links = []
        for i in range(9):
            line_strong_links = self.sudoku.get_n_optioned_unit(i, Unit.LINE, 2)
            column_strong_links = self.sudoku.get_n_optioned_unit(i, Unit.COLUMN, 2)
            block_strong_links = self.sudoku.get_n_optioned_unit(i, Unit.BLOCK, 2)
            links += line_strong_links + column_strong_links + block_strong_links
        return links

    @staticmethod
    def _get_strong_link_mapping(strong_links: list[Link]) -> tuple[dict[int, Mapping], list[Cell]]:
        mapping = {i: {} for i in range(9)}
        cells = []
        for link in strong_links:
            value = link[0].values[0]
            cell_1, cell_2 = link
            position_1, position_2 = cell_1.position, cell_2.position
            mapping_1 = mapping[value][position_1] if position_1 in mapping[value].keys() else []
            mapping_2 = mapping[value][position_2] if position_2 in mapping[value].keys() else []
            mapping[value][position_1] = mapping_1 + [cell_2]
            mapping[value][position_2] = mapping_2 + [cell_1]
            cells += [cell_1, cell_2]
        return mapping, list(set(cells))

    def _get_medusas(self) -> list[Medusa]:
        strong_links = self.get_strong_links()
        strong_link_mapping, cells = self._get_strong_link_mapping(strong_links)
        medusas = []
        elements_without_group = set(cells)
        while len(elements_without_group) > 0:
            element = elements_without_group.pop()
            medusa = self._get_medusa(element, strong_link_mapping)
            medusas.append(medusa)
            elements_without_group -= set(medusa.cells)
        return medusas

    def _get_medusa(self, cell: Cell, strong_link_mapping: dict[int, Mapping]) -> Medusa:
        medusa = Medusa()
        new_nodes = [Node(cell, 1)]
        while len(new_nodes) > 0:
            for node in new_nodes:
                medusa.add_node(node)
            new_nodes = self._get_new_nodes(medusa, strong_link_mapping, new_nodes)
        return medusa

    def _get_new_nodes(self, medusa: Medusa, strong_link_mapping: dict[int, Mapping], nodes: list[Node]) -> list[Node]:
        new_nodes = []
        for node in nodes:
            other_values = list(set(self.sudoku.get_values_for_position(node.position)) - {node.value})
            if len(other_values) == 1:
                new_nodes.append(Node(Cell(node.line, node.column, (other_values[0],)), 1 - node.color))
                # value = other_values[0]
                # if value in strong_link_mapping.keys() and node.position in strong_link_mapping[value].keys():
                #     new_nodes.append(Node(Cell(node.line, node.column, (value,)), 1 - node.color))
                #     for element in strong_link_mapping[value][node.position]:
                #         new_nodes.append(Node(Cell(element.line, element.column, (value,)), node.color))
            if node.value in strong_link_mapping.keys() and node.position in strong_link_mapping[node.value].keys():
                new_nodes += [Node(cell, 1 - node.color) for cell in strong_link_mapping[node.value][node.position]]
        return list(filter(lambda node: node.cell not in medusa.cells, new_nodes))

    def _rule_1(self, medusa: Medusa) -> None:
        position_color_mapping: dict[Position, dict[int, int]] = {}
        for node in medusa.nodes:
            if node.position not in position_color_mapping.keys():
                position_color_mapping[node.position] = {0: 0, 1: 0}
            position_color_mapping[node.position][node.color] += 1
        for colors in position_color_mapping.values():
            for color in range(0, 2):
                if colors[color] > 1:
                    nodes = list(filter(lambda node: node.color == color, medusa.nodes))
                    for node in nodes:
                        self.sudoku.possible_values_grid[node.line, node.column, node.value] = 0
                    return

    def _rule_2(self, medusa: Medusa) -> None:
        for value in range(9):
            for i in range(9):
                nodes_on_line = list(filter(lambda node: node.line == i and node.value == value, medusa.nodes))
                if self._update_rule_2(medusa, nodes_on_line):
                    return
            for j in range(9):
                nodes_on_column = list(filter(lambda node: node.column == j and node.value == value, medusa.nodes))
                if self._update_rule_2(medusa, nodes_on_column):
                    return
            for y in range(3):
                for x in range(3):
                    nodes_on_column = list(
                        filter(lambda node: node.line // 3 == y and node.column // 3 == x and node.value == value,
                               medusa.nodes))
                    if self._update_rule_2(medusa, nodes_on_column):
                        return

    def _update_rule_2(self, medusa: Medusa, nodes: list[Node]) -> bool:
        colors = {0: 0, 1: 0}
        for node in nodes:
            colors[node.color] += 1
        for color in range(0, 2):
            if colors[color] > 1:
                nodes = list(filter(lambda node: node.color == color, medusa.nodes))
                for node in nodes:
                    self.sudoku.possible_values_grid[node.line, node.column, node.value] = 0
                return True
        return False

    def _rule_3(self, medusa: Medusa) -> None:
        positions = set(map(lambda node: node.position, medusa.nodes))
        for position in positions:
            nodes = list(filter(lambda node: node.position == position, medusa.nodes))
            colors = {0: 0, 1: 0}
            values = []
            for node in nodes:
                values.append(node.value)
                colors[node.color] += 1
            if colors[0] > 0 and colors[1] > 0:
                joined_values = list(set(range(9)) - set(values))
                self.sudoku.possible_values_grid[position[0], position[1], joined_values] = 0

    def _rule_4(self, medusa: Medusa) -> None:
        for value in range(9):
            nodes = list(filter(lambda node: node.value == value, medusa.nodes))
            color_mapping: dict[int, list[Node]] = {0: [], 1: []}
            for node in nodes:
                color_mapping[node.color].append(node)
            couples = [(node_1, node_2) for node_1 in color_mapping[0] for node_2 in color_mapping[1]]
            for node_1, node_2 in couples:
                positions = self._get_bi_visible_cells(node_1.position, node_2.position)
                for position in positions:
                    if position not in medusa.positions:
                        self.sudoku.possible_values_grid[position[0], position[1], value] = 0

    def _rule_5(self, medusa: Medusa) -> None:
        cell_value_mapping: dict[Position, ColoredCell] = {}
        for position in medusa.positions:
            values = self.sudoku.get_values_for_position(position)
            cell_value_mapping[position] = ColoredCell(position, values)
        for node in medusa.nodes:
            cell_value_mapping[node.position].color(node)
            positions = get_visibility(node.position)
            for position in positions:
                if position in medusa.positions:
                    cell_value_mapping[position].color_from_visible(node)

        for cell in cell_value_mapping.values():
            for color in range(2):
                for value in cell.uncolored:
                    if len(cell.colored[color]) > 0 and value in cell.visible_value_color[1 - color]:
                        self.sudoku.possible_values_grid[cell.line, cell.column, value] = 0

    def _rule_6(self, medusa: Medusa) -> None:
        y_pos, x_pos = np.where(self.sudoku.grid == 0)
        out_of_medusa_positions: set[Position] = set(zip(y_pos, x_pos)) - set(medusa.positions)
        cell_value_mapping: dict[Position, ColoredCell] = {}
        for position in out_of_medusa_positions:
            values = self.sudoku.get_values_for_position(position)
            cell_value_mapping[position] = ColoredCell(position, values)
        for node in medusa.nodes:
            positions = get_visibility(node.position)
            for position in positions:
                if position in out_of_medusa_positions:
                    cell_value_mapping[position].color_from_visible(node)

        updated = False
        for cell in cell_value_mapping.values():
            for color in range(2):
                if len(cell.visible_value_color[color]) == len(cell.values):
                    updated = True
                    for node in medusa.nodes:
                        if node.color == color:
                            self.sudoku.possible_values_grid[node.line, node.column, node.value] = 0
                if updated:
                    return

    @staticmethod
    def _get_bi_visible_cells(position_1: Position, position_2: Position) -> list[Position]:
        visibility_1, visibility_2 = get_visibility(position_1), get_visibility(position_2)
        bi_visible_cells = []
        for position in visibility_1:
            if position in visibility_2:
                bi_visible_cells.append(position)
        return list(set(bi_visible_cells) - {position_1, position_2})


def get_visibility(position: Position) -> list[Position]:
    positions = []
    u, v = 3 * (position[0] // 3), 3 * (position[1] // 3)
    positions += [(i, position[1]) for i in range(9)]
    positions += [(position[0], j) for j in range(9)]
    positions += [(i, j) for i in range(u, u + 3) for j in range(v, v + 3)]
    return list(set(positions) - {position})


class ColoredCell:
    def __init__(self, position: Position, values: list[int]) -> None:
        self.position = position
        self.values = values
        self.colored = {0: [], 1: []}
        self.uncolored = values
        self.visible_value_color = {0: [], 1: []}

    def color(self, node: Node) -> None:
        self.colored[node.color].append(node)
        self.uncolored = list(set(self.uncolored) - {node.value})

    def color_from_visible(self, node) -> None:
        if node.value in self.values and node.value not in self.visible_value_color[node.color]:
            self.visible_value_color[node.color].append(node.value)

    @property
    def line(self) -> int:
        return self.position[0]

    @property
    def column(self) -> int:
        return self.position[1]