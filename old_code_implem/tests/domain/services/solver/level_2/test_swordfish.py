from src.domain.services.solver import Solver
from src.domain.services.strategies_level_1.hidden_candidates import HiddenCandidates
from src.domain.services.strategies_level_1.intersection_removal import IntersectionRemoval
from src.domain.services.strategies_level_1.naked_candidates import NakedCandidates
from src.domain.services.strategies_level_2.swordfish import Swordfish
from tests import data
import os


class TestSwordfish:
    def test_swordfish(self) -> None:
        # Given
        file = os.path.dirname(data.__file__) + "\\test_swordfish.csv"
        strategies = [
            IntersectionRemoval,
            NakedCandidates,
            HiddenCandidates,
            Swordfish,
        ]
        solver = Solver.from_csv(file, strategies)

        # When
        solved = solver._solve()

        # Then
        assert solved is True

    def test_swordfish_bis(self) -> None:
        # Given
        file = os.path.dirname(data.__file__) + "\\test_swordfish.csv"
        strategies = [
            IntersectionRemoval,
            NakedCandidates,
            HiddenCandidates,
            Swordfish,
        ]
        solver = Solver.from_csv(file, strategies)

        # When
        solved = solver._solve()

        # Then
        assert solved is True

    def test_swordfish_ter(self) -> None:
        # Given
        file = os.path.dirname(data.__file__) + "\\test_swordfish.csv"
        strategies = [
            IntersectionRemoval,
            NakedCandidates,
            HiddenCandidates,
            Swordfish,
        ]
        solver = Solver.from_csv(file, strategies)

        # When
        solved = solver._solve()

        # Then
        assert solved is True
