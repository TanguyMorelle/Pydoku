from src.domain.services.solver import Solver
from src.domain.services.strategies_level_1.hidden_candidates import HiddenCandidates
from src.domain.services.strategies_level_1.intersection_removal import IntersectionRemoval
from src.domain.services.strategies_level_1.naked_candidates import NakedCandidates
from src.domain.services.strategies_level_3.x_chain import XChains
from tests import data
import os


class TestXChains:
    def test_x_chains(self) -> None:
        # Given
        file = os.path.dirname(data.__file__) + "\\test_x_chains.csv"
        strategies = [
            IntersectionRemoval,
            NakedCandidates,
            HiddenCandidates,
            XChains,
        ]
        solver = Solver.from_csv(file, strategies)

        # When
        solved = solver._solve()

        # Then
        assert solved is True

    def test_x_chains_bis(self) -> None:
        # Given
        file = os.path.dirname(data.__file__) + "\\test_x_chains_2.csv"
        strategies = [
            IntersectionRemoval,
            NakedCandidates,
            HiddenCandidates,
            XChains,
        ]
        solver = Solver.from_csv(file, strategies)

        # When
        solved = solver._solve()

        # Then
        assert solved is True
