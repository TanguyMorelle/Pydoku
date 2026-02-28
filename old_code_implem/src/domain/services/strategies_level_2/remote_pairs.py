from src.domain.models.cell import Cell
from src.domain.models.sudoku import Sudoku
from src.domain.services.strategies_level_2.single_chains import SingleChains
from src.domain.services.strategy import Strategy
from src.warnings import deprecated

Position = tuple[int, int]
Chain = list[Position]
Cycle = dict[Position: Chain]


@deprecated(SingleChains)
class RemotePairs(Strategy):

    def __init__(self, sudoku: Sudoku) -> None:
        super().__init__(sudoku)

    def execute(self) -> None:
        bi_value_cells = self.sudoku.get_n_valued_cells(self.sudoku.possible_values_grid, 2)
        value_pairs = set(map(lambda cell: cell.values, bi_value_cells))
        for pair in value_pairs:
            valid_cells = list(filter(lambda cell: cell.values == pair, bi_value_cells))
            cycle = self._get_cycle(valid_cells)
            self._remote_pairs(pair, cycle)

    def _remote_pairs(self, pair: list[int, int], cycle: Cycle) -> None:
        for element in cycle:
            complementary_chain = self._get_chain(cycle, cycle[element])
            for complementary in complementary_chain:
                if element[0] != complementary[0] and element[1] != complementary[1]:
                    for value in pair:
                        if (element[0], complementary[1]) not in cycle:
                            self.sudoku.possible_values_grid[element[0], complementary[1], value] = 0
                        if (complementary[0], element[1]) not in cycle:
                            self.sudoku.possible_values_grid[complementary[0], element[1], value] = 0

    def _get_cycle(self, cells: list[Cell]) -> Cycle:
        cycle = {cell.position: [] for cell in cells}
        for i in range(len(cells)):
            p1 = cells[i].position
            for j in range(i + 1, len(cells)):
                p2 = cells[j].position
                if cells[i].check_visibility(cells[j]):
                    cycle[p1].append(p2)
                    cycle[p2].append(p1)
        return cycle

    def _get_chain(self, cycle: Cycle, chain: Chain) -> Chain:
        chain_elements = []
        for element in chain:
            for link in cycle[element]:
                chain_elements += cycle[link]
        new_elements = set(chain_elements) - set(chain)
        chain += list(new_elements)
        if len(new_elements) > 0:
            chain = self._get_chain(cycle, chain)
        return chain
