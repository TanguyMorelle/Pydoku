from src.domain.services.solver import Solver
from src.domain.services.strategies_level_1.hidden_candidates import HiddenCandidates
from src.domain.services.strategies_level_1.intersection_removal import IntersectionRemoval
from src.domain.services.strategies_level_1.naked_candidates import NakedCandidates
from src.domain.services.strategies_level_3.x_chain import XChains
from src.domain.services.strategies_level_3.x_cycles import XCycles
from tests import data
import os


class TestXCycles:
    def test_x_cycle_rule_2(self) -> None:
        # Given
        file = os.path.dirname(data.__file__) + "\\test_x_cycles_rule_2.csv"
        strategies = [
            IntersectionRemoval,
            NakedCandidates,
            HiddenCandidates,
            XCycles,
        ]
        solver = Solver.from_csv(file, strategies)

        # When
        solved = solver._solve()

        # Then
        assert solved is True
