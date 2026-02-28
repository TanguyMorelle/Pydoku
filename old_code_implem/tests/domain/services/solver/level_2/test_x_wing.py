from src.domain.services.solver import Solver
from src.domain.services.strategies_level_1.hidden_candidates import HiddenCandidates
from src.domain.services.strategies_level_1.intersection_removal import IntersectionRemoval
from src.domain.services.strategies_level_1.naked_candidates import NakedCandidates
from src.domain.services.strategies_level_2.x_wing import XWing
from tests import data
import os


class TestXWing:
    def test_x_wing(self) -> None:
        # Given
        file = os.path.dirname(data.__file__) + "\\test_x_wing.csv"
        strategies = [
            IntersectionRemoval,
            NakedCandidates,
            HiddenCandidates,
            XWing,
        ]
        solver = Solver.from_csv(file, strategies)

        # When
        solved = solver._solve()

        # Then
        assert solved is True
