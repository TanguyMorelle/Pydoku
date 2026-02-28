from src.domain.services.solver import Solver
from src.domain.services.strategies_level_1.hidden_candidates import HiddenCandidates
from src.domain.services.strategies_level_1.intersection_removal import IntersectionRemoval
from src.domain.services.strategies_level_1.naked_candidates import NakedCandidates
from src.domain.services.strategies_level_2.xyz_wing import XYZWing
from tests import data
import os


class TestXWing:
    def test_xyz_wing(self) -> None:
        # Given
        file = os.path.dirname(data.__file__) + "\\test_xyz_wing.csv"
        strategies = [
            IntersectionRemoval,
            NakedCandidates,
            HiddenCandidates,
            XYZWing,
        ]
        solver = Solver.from_csv(file, strategies)

        # When
        solved = solver._solve()

        # Then
        assert solved is True
