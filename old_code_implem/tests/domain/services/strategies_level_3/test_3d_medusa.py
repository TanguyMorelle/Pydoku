import numpy as np

from src.domain.models.cell import Cell
from src.domain.models.sudoku import Sudoku
from src.domain.services.strategies_level_3.d3_medusa import D3Medusa, Medusa, Node


class Test3dMedusa:
    def test_get_medusas(self) -> None:
        # Given
        sudoku = Sudoku(np.zeros((9, 9)))
        sudoku.possible_values_grid = np.zeros((9, 9, 9))
        cells = [
            Cell(0, 0, (0, 6)),
            Cell(0, 8, (0, 6)),

            Cell(1, 0, (0, 3, 6)),
            Cell(1, 4, (2, 8)),
            Cell(1, 5, (0, 2)),
            Cell(1, 6, (3, 8)),
            Cell(1, 7, (0, 2, 6)),

            Cell(2, 1, (0, 3)),
            Cell(2, 3, (0, 2, 8)),
            Cell(2, 6, (3, 8)),
            Cell(2, 7, (0, 2)),

            Cell(4, 0, (3, 5, 8)),
            Cell(4, 1, (3, 5)),
            Cell(4, 2, (3, 8)),
            Cell(4, 7, (0, 6)),
            Cell(4, 8, (0, 6)),

            Cell(5, 3, (0, 2)),
            Cell(5, 5, (0, 2)),

            Cell(6, 2, (3, 8)),
            Cell(6, 3, (3, 8)),

            Cell(7, 0, (0, 3, 8)),
            Cell(7, 1, (0, 2, 3)),
            Cell(7, 3, (2, 3, 8)),
            Cell(7, 8, (3, 8)),

            Cell(8, 0, (3, 5, 8)),
            Cell(8, 1, (2, 3, 5)),
            Cell(8, 4, (2, 8)),
            Cell(8, 8, (3, 8)),
        ]

        for cell in cells:
            sudoku.possible_values_grid[cell.line, cell.column, cell.values] = 1

        medusa = D3Medusa(sudoku)

        nodes_0 = [
            Node(Cell(4, 0, (8,)), 1),
            Node(Cell(4, 2, (8,)), 0),
            Node(Cell(4, 2, (3,)), 1),
            Node(Cell(6, 2, (8,)), 1),
            Node(Cell(6, 2, (3,)), 0),
            Node(Cell(6, 3, (8,)), 0),
            Node(Cell(6, 3, (3,)), 1),
            Node(Cell(7, 3, (3,)), 0),
        ]
        nodes_1 = [
            Node(Cell(4, 0, (5,)), 1),
            Node(Cell(4, 1, (5,)), 0),
            Node(Cell(8, 0, (5,)), 0),
            Node(Cell(4, 1, (3,)), 1),
            Node(Cell(8, 1, (5,)), 1),
        ]
        nodes_2 = [
            Node(Cell(1, 0, (6,)), 1),
            Node(Cell(1, 7, (6,)), 0),
            Node(Cell(0, 0, (6,)), 0),
            Node(Cell(4, 7, (6,)), 1),
            Node(Cell(0, 8, (6,)), 1),
            Node(Cell(0, 0, (0,)), 1),
            Node(Cell(4, 7, (0,)), 0),
            Node(Cell(4, 8, (6,)), 0),
            Node(Cell(0, 8, (0,)), 0),
            Node(Cell(4, 8, (0,)), 1),
        ]
        nodes_3 = [
            Node(Cell(1, 6, (8,)), 1),
            Node(Cell(1, 6, (3,)), 0),
            Node(Cell(1, 4, (8,)), 0),
            Node(Cell(2, 6, (8,)), 0),
            Node(Cell(1, 0, (3,)), 1),
            Node(Cell(2, 6, (3,)), 1),
            Node(Cell(1, 4, (2,)), 1),
            Node(Cell(8, 4, (8,)), 1),
            Node(Cell(2, 3, (8,)), 1),
            Node(Cell(2, 1, (3,)), 0),
            Node(Cell(8, 4, (2,)), 0),
            Node(Cell(2, 1, (0,)), 1),
            Node(Cell(8, 1, (2,)), 1),
            Node(Cell(7, 3, (2,)), 1),
            Node(Cell(7, 1, (0,)), 0),
            Node(Cell(7, 1, (2,)), 0),
            Node(Cell(7, 0, (0,)), 1),
        ]
        nodes_4 = [
            Node(Cell(5, 5, (0,)), 1),
            Node(Cell(5, 5, (2,)), 0),
            Node(Cell(5, 3, (0,)), 0),
            Node(Cell(1, 5, (0,)), 0),
            Node(Cell(5, 3, (2,)), 1),
            Node(Cell(1, 5, (2,)), 1),
            Node(Cell(2, 3, (0,)), 1),
        ]
        nodes_5 = [
            Node(Cell(2, 3, (2,)), 1),
            Node(Cell(2, 7, (2,)), 0),
            Node(Cell(2, 7, (0,)), 1),
            Node(Cell(1, 7, (2,)), 1),
        ]
        nodes_6 = [
            Node(Cell(7, 8, (8,)), 1),
            Node(Cell(7, 8, (3,)), 0),
            Node(Cell(8, 8, (8,)), 0),
            Node(Cell(8, 8, (3,)), 1),
        ]

        medusa_0 = Medusa()
        medusa_1 = Medusa()
        medusa_2 = Medusa()
        medusa_3 = Medusa()
        medusa_4 = Medusa()
        medusa_5 = Medusa()
        medusa_6 = Medusa()

        for node in nodes_0: medusa_0.add_node(node)
        for node in nodes_1: medusa_1.add_node(node)
        for node in nodes_2: medusa_2.add_node(node)
        for node in nodes_3: medusa_3.add_node(node)
        for node in nodes_4: medusa_4.add_node(node)
        for node in nodes_5: medusa_5.add_node(node)
        for node in nodes_6: medusa_6.add_node(node)

        # When
        medusas = medusa._get_medusas()

        # Then
        assert len(medusas) == 7
        assert medusa_0 in medusas
        assert medusa_1 in medusas
        assert medusa_2 in medusas
        assert medusa_3 in medusas
        assert medusa_4 in medusas
        assert medusa_5 in medusas
        assert medusa_6 in medusas

    def test_rule_1(self) -> None:
        # Given
        sudoku = Sudoku(np.zeros((9, 9)))
        sudoku.possible_values_grid = np.zeros((9, 9, 9))
        cells = [
            Cell(0, 0, (0, 6)),
            Cell(0, 8, (0, 6)),

            Cell(1, 0, (0, 3, 6)),
            Cell(1, 4, (2, 8)),
            Cell(1, 5, (0, 2)),
            Cell(1, 6, (3, 8)),
            Cell(1, 7, (0, 2, 6)),

            Cell(2, 1, (0, 3)),
            Cell(2, 3, (0, 2, 8)),
            Cell(2, 6, (3, 8)),
            Cell(2, 7, (0, 2)),

            Cell(4, 0, (3, 5, 8)),
            Cell(4, 1, (3, 5)),
            Cell(4, 2, (3, 8)),
            Cell(4, 7, (0, 6)),
            Cell(4, 8, (0, 6)),

            Cell(5, 3, (0, 2)),
            Cell(5, 5, (0, 2)),

            Cell(6, 2, (3, 8)),
            Cell(6, 3, (3, 8)),

            Cell(7, 0, (0, 3, 8)),
            Cell(7, 1, (0, 2, 3)),
            Cell(7, 3, (2, 3, 8)),
            Cell(7, 8, (3, 8)),

            Cell(8, 0, (3, 5, 8)),
            Cell(8, 1, (2, 3, 5)),
            Cell(8, 4, (2, 8)),
            Cell(8, 8, (3, 8)),
        ]

        for cell in cells:
            sudoku.possible_values_grid[cell.line, cell.column, cell.values] = 1

        nodes = [
            Node(Cell(1, 6, (8,)), 1),
            Node(Cell(1, 6, (3,)), 0),
            Node(Cell(1, 4, (8,)), 0),
            Node(Cell(2, 6, (8,)), 0),
            Node(Cell(1, 0, (3,)), 1),
            Node(Cell(2, 6, (3,)), 1),
            Node(Cell(1, 4, (2,)), 1),
            Node(Cell(8, 4, (8,)), 1),
            Node(Cell(2, 3, (8,)), 1),
            Node(Cell(2, 1, (3,)), 0),
            Node(Cell(8, 4, (2,)), 0),
            Node(Cell(2, 1, (0,)), 1),
            Node(Cell(8, 1, (2,)), 1),
            Node(Cell(7, 3, (2,)), 1),
            Node(Cell(7, 1, (0,)), 0),
            Node(Cell(7, 1, (2,)), 0),
            Node(Cell(7, 0, (0,)), 1),
        ]
        medusa = Medusa()
        for node in nodes: medusa.add_node(node)

        d3_medusa = D3Medusa(sudoku)

        # When
        d3_medusa._rule_1(medusa)

        # Then
        for cell in set(cells):
            if cell.position not in medusa.positions:
                for value in cell.values:
                    assert d3_medusa.sudoku.possible_values_grid[cell.line, cell.column, value] == 1
        for node in nodes:
            if node.color == 0:
                assert d3_medusa.sudoku.possible_values_grid[node.line, node.column, node.value] == 0
            else:
                assert d3_medusa.sudoku.possible_values_grid[node.line, node.column, node.value] == 1

    def test_rule_2(self) -> None:
        # Given
        sudoku = Sudoku(np.zeros((9, 9)))
        sudoku.possible_values_grid = np.zeros((9, 9, 9))
        cells = [
            Cell(0, 6, (3, 5)),
            Cell(0, 7, (3,)),
            Cell(1, 2, (5,)),
            Cell(1, 6, (5, 6)),
            Cell(3, 4, (6,)),
            Cell(3, 7, (3, 6)),
            Cell(4, 5, (3,)),
            Cell(4, 6, (3,)),
            Cell(5, 3, (6, 8)),
            Cell(5, 6, (8,)),
            Cell(8, 3, (6,)),
            Cell(8, 6, (6,)),
        ]

        for cell in cells:
            sudoku.possible_values_grid[cell.line, cell.column, cell.values] = 1

        nodes = [
            Node(Cell(0, 6, (3,)), 1),
            Node(Cell(0, 6, (5,)), 0),
            Node(Cell(0, 7, (3,)), 0),
            Node(Cell(1, 2, (5,)), 0),
            Node(Cell(1, 6, (5,)), 1),
            Node(Cell(1, 6, (6,)), 0),
            Node(Cell(3, 4, (6,)), 1),
            Node(Cell(3, 7, (3,)), 1),
            Node(Cell(3, 7, (6,)), 0),
            Node(Cell(4, 5, (3,)), 1),
            Node(Cell(4, 6, (3,)), 0),
            Node(Cell(5, 3, (6,)), 0),
            Node(Cell(5, 3, (8,)), 1),
            Node(Cell(5, 6, (8,)), 0),
            Node(Cell(8, 3, (6,)), 1),
            Node(Cell(8, 6, (6,)), 0),
        ]
        medusa = Medusa()
        for node in nodes: medusa.add_node(node)

        d3_medusa = D3Medusa(sudoku)

        # When
        d3_medusa._rule_2(medusa)

        # Then
        for node in nodes:
            if node.color == 0:
                assert d3_medusa.sudoku.possible_values_grid[node.line, node.column, node.value] == 0
            else:
                assert d3_medusa.sudoku.possible_values_grid[node.line, node.column, node.value] == 1

    def test_rule_3(self) -> None:
        # Given
        sudoku = Sudoku(np.zeros((9, 9)))
        sudoku.possible_values_grid = np.zeros((9, 9, 9))
        cells = [
            Cell(2, 0, (2, 4, 6)),
            Cell(2, 1, (2, 6, 7)),
            Cell(5, 0, (2, 6)),
            Cell(5, 1, (1, 2, 6)),
        ]

        for cell in cells:
            sudoku.possible_values_grid[cell.line, cell.column, cell.values] = 1

        nodes = [
            Node(Cell(2, 6, (2,)), 1),
            Node(Cell(2, 1, (2,)), 0),
            Node(Cell(2, 1, (6,)), 1),
            Node(Cell(5, 1, (6,)), 0),
            Node(Cell(5, 0, (6,)), 1),
            Node(Cell(5, 0, (2,)), 0),
        ]
        medusa = Medusa()
        for node in nodes: medusa.add_node(node)

        d3_medusa = D3Medusa(sudoku)

        # When
        d3_medusa._rule_3(medusa)

        # Then
        assert d3_medusa.sudoku.possible_values_grid[2, 1, 7] == 0
        assert d3_medusa.sudoku.possible_values_grid[2, 1, 2] == 1
        assert d3_medusa.sudoku.possible_values_grid[2, 1, 6] == 1
        for cell in cells:
            if cell.position != (2, 1):
                for value in cell.values:
                    assert d3_medusa.sudoku.possible_values_grid[cell.line, cell.column, value] == 1

    def test_rule_4(self) -> None:
        # Given
        sudoku = Sudoku(np.zeros((9, 9)))
        sudoku.possible_values_grid = np.zeros((9, 9, 9))
        cells = [
            Cell(1, 0, (1, 4, 5)),
            Cell(1, 8, (5, 7)),
            Cell(2, 1, (5, 6, 8)),
            Cell(2, 7, (4, 5, 8)),
            Cell(5, 8, (3, 5, 8)),
            Cell(7, 0, (1, 3, 4, 5)),
            Cell(7, 1, (5, 7)),
            Cell(7, 8, (3, 7)),
            Cell(8, 1, (7, 8)),
            Cell(8, 2, (1, 3, 4, 8)),
            Cell(8, 7, (1, 3, 7)),
        ]

        for cell in cells:
            sudoku.possible_values_grid[cell.line, cell.column, cell.values] = 1

        nodes = [
            Node(Cell(5, 8, (5,)), 1),
            Node(Cell(1, 8, (5,)), 0),
            Node(Cell(1, 8, (7,)), 1),
            Node(Cell(7, 8, (7,)), 1),
            Node(Cell(7, 8, (3,)), 0),
            Node(Cell(8, 7, (7,)), 1),
            Node(Cell(8, 1, (7,)), 0),
            Node(Cell(8, 1, (8,)), 1),
            Node(Cell(8, 2, (8,)), 0),
            Node(Cell(7, 1, (7,)), 1),
            Node(Cell(7, 1, (5,)), 0),
            Node(Cell(7, 0, (5,)), 1),
            Node(Cell(2, 1, (5,)), 1),
        ]

        medusa = Medusa()
        for node in nodes: medusa.add_node(node)

        d3_medusa = D3Medusa(sudoku)

        # When
        d3_medusa._rule_4(medusa)

        # Then
        assert d3_medusa.sudoku.possible_values_grid[1, 0, 5] == 0
        assert d3_medusa.sudoku.possible_values_grid[1, 0, 1] == 1
        assert d3_medusa.sudoku.possible_values_grid[1, 0, 4] == 1
        assert d3_medusa.sudoku.possible_values_grid[2, 7, 5] == 0
        assert d3_medusa.sudoku.possible_values_grid[2, 7, 4] == 1
        assert d3_medusa.sudoku.possible_values_grid[2, 7, 8] == 1
        for cell in cells:
            if cell.position not in [(1, 0), (2, 7)]:
                for value in cell.values:
                    assert d3_medusa.sudoku.possible_values_grid[cell.line, cell.column, value] == 1

    def test_rule_5(self) -> None:
        # Given
        sudoku = Sudoku(np.zeros((9, 9)))
        sudoku.possible_values_grid = np.zeros((9, 9, 9))
        cells = [
            Cell(2, 4, (5, 7, 8)),
            Cell(2, 5, (5, 8)),
            Cell(2, 6, (5, 6, 7)),
            Cell(2, 8, (6, 7)),

            Cell(3, 3, (2, 4, 7)),
            Cell(3, 8, (2, 7)),

            Cell(4, 3, (0, 5, 7)),
            Cell(4, 4, (0, 5, 6)),
            Cell(4, 5, (0, 5)),
            Cell(4, 6, (6, 7)),

            Cell(5, 3, (2, 8)),
            Cell(5, 4, (6, 8)),
            Cell(5, 8, (2, 6)),

            Cell(7, 3, (0, 4, 8)),
            Cell(7, 5, (0, 4, 8)),
        ]

        for cell in cells:
            sudoku.possible_values_grid[cell.line, cell.column, cell.values] = 1

        nodes = [
            Node(Cell(2, 4, (8,)), 1),
            Node(Cell(2, 5, (5,)), 1),
            Node(Cell(2, 5, (8,)), 0),
            Node(Cell(2, 6, (6,)), 0),
            Node(Cell(2, 8, (6,)), 1),
            Node(Cell(2, 8, (7,)), 0),
            Node(Cell(3, 3, (7,)), 0),
            Node(Cell(3, 8, (2,)), 0),
            Node(Cell(3, 8, (7,)), 1),
            Node(Cell(4, 3, (7,)), 1),
            Node(Cell(4, 4, (6,)), 0),
            Node(Cell(4, 5, (0,)), 1),
            Node(Cell(4, 5, (5,)), 0),
            Node(Cell(4, 6, (6,)), 1),
            Node(Cell(4, 6, (7,)), 0),
            Node(Cell(5, 3, (2,)), 0),
            Node(Cell(5, 3, (8,)), 1),
            Node(Cell(5, 4, (6,)), 1),
            Node(Cell(5, 4, (8,)), 0),
            Node(Cell(5, 8, (2,)), 1),
            Node(Cell(5, 8, (6,)), 0),
            Node(Cell(7, 3, (8,)), 0),
            Node(Cell(7, 5, (8,)), 1),
        ]

        medusa = Medusa()
        for node in nodes: medusa.add_node(node)

        d3_medusa = D3Medusa(sudoku)

        # When
        d3_medusa._rule_5(medusa)

        # Then
        assert d3_medusa.sudoku.possible_values_grid[2, 4, 7] == 0
        assert d3_medusa.sudoku.possible_values_grid[2, 4, 5] == 1
        assert d3_medusa.sudoku.possible_values_grid[2, 4, 8] == 1

        assert d3_medusa.sudoku.possible_values_grid[2, 6, 5] == 0
        assert d3_medusa.sudoku.possible_values_grid[2, 6, 6] == 1
        assert d3_medusa.sudoku.possible_values_grid[2, 6, 7] == 1

        assert d3_medusa.sudoku.possible_values_grid[4, 3, 5] == 0
        assert d3_medusa.sudoku.possible_values_grid[4, 3, 0] == 1
        assert d3_medusa.sudoku.possible_values_grid[4, 3, 7] == 1

        assert d3_medusa.sudoku.possible_values_grid[4, 4, 0] == 0
        assert d3_medusa.sudoku.possible_values_grid[4, 4, 5] == 1
        assert d3_medusa.sudoku.possible_values_grid[4, 4, 6] == 1

        for cell in cells:
            if cell.position not in [(2, 4), (2, 6), (4, 3), (4, 4)]:
                for value in cell.values:
                    assert d3_medusa.sudoku.possible_values_grid[cell.line, cell.column, value] == 1

    def test_rule_6(self) -> None:
        # Given
        sudoku = Sudoku(np.zeros((9, 9)))
        sudoku.possible_values_grid = np.zeros((9, 9, 9))
        cells = [
            Cell(1, 1, (0, 1)),
            Cell(1, 6, (1, 7)),
            Cell(1, 7, (0, 1, 7)),

            Cell(2, 0, (1, 4)),
            Cell(2, 1, (0, 1, 4)),
            Cell(2, 3, (3, 7)),
            Cell(2, 5, (3, 7)),
            Cell(2, 8, (0, 1)),

            Cell(3, 0, (1, 3, 7)),
            Cell(3, 3, (1, 3, 7)),
            Cell(3, 6, (0, 3, 7)),
            Cell(3, 7, (0, 7)),

            Cell(4, 2, (1, 7)),
            Cell(4, 3, (1, 3, 7)),
            Cell(4, 6, (3, 4, 7)),
            Cell(4, 7, (4, 7)),

            Cell(5, 1, (3, 4)),
            Cell(5, 2, (4, 7)),
            Cell(5, 5, (3, 7)),

            Cell(6, 0, (1, 3, 4, 7)),
            Cell(6, 1, (1, 3, 4)),
            Cell(6, 2, (1, 4, 7)),
            Cell(6, 6, (0, 4)),
            Cell(6, 8, (0, 1, 7)),

            Cell(7, 0, (1, 4, 7)),
            Cell(7, 7, (1, 4)),
            Cell(7, 8, (1, 7)),
        ]

        for cell in cells:
            sudoku.possible_values_grid[cell.line, cell.column, cell.values] = 1

        nodes = [
            Node(Cell(1, 1, (0,)), 1),
            Node(Cell(1, 1, (1,)), 0),
            Node(Cell(1, 7, (1,)), 1),
            Node(Cell(2, 1, (0,)), 0),
            Node(Cell(2, 8, (0,)), 1),
            Node(Cell(7, 7, (1,)), 0),
            Node(Cell(6, 6, (0,)), 1),
            Node(Cell(2, 8, (1,)), 0),
            Node(Cell(4, 6, (4,)), 1),
            Node(Cell(6, 8, (0,)), 0),
            Node(Cell(4, 7, (7,)), 1),
            Node(Cell(4, 7, (4,)), 0),
            Node(Cell(7, 7, (4,)), 1),
            Node(Cell(6, 6, (4,)), 0),
            Node(Cell(7, 0, (4,)), 0),
        ]

        medusa = Medusa()
        for node in nodes: medusa.add_node(node)

        d3_medusa = D3Medusa(sudoku)

        # When
        d3_medusa._rule_6(medusa)

        # Then
        for node in nodes:
            if node.color == 0:
                assert d3_medusa.sudoku.possible_values_grid[node.line, node.column, node.value] == 0
            else:
                assert d3_medusa.sudoku.possible_values_grid[node.line, node.column, node.value] == 1
