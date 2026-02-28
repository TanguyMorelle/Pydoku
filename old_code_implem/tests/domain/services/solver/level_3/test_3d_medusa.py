from src.domain.services.solver import Solver
from src.domain.services.strategies_level_1.hidden_candidates import HiddenCandidates
from src.domain.services.strategies_level_1.intersection_removal import IntersectionRemoval
from src.domain.services.strategies_level_1.naked_candidates import NakedCandidates
from src.domain.services.strategies_level_2.xyz_wing import XYZWing
from src.domain.services.strategies_level_3.d3_medusa import D3Medusa
from src.domain.services.strategies_level_3.x_chain import XChains
from src.domain.services.strategies_level_3.x_cycles import XCycles
from src.domain.services.strategies_level_3.xy_chains import XYChains
from tests import data
import os


class Test3DMedusa:
    def test_3d_medusa_rule_1(self) -> None:
        # Given
        file = os.path.dirname(data.__file__) + "\\test_3d_medusa_rule_1.csv"
        strategies = [
            IntersectionRemoval,
            NakedCandidates,
            HiddenCandidates,
            D3Medusa,
        ]
        solver = Solver.from_csv(file, strategies)

        # When
        solved = solver._solve()

        # Then
        assert solved is True

    def test_3d_medusa_rule_2(self) -> None:
        # Given
        file = os.path.dirname(data.__file__) + "\\test_3d_medusa_rule_2.csv"
        strategies = [
            IntersectionRemoval,
            NakedCandidates,
            HiddenCandidates,
            XYZWing,
            XChains,
            XCycles,
            XYChains,
            D3Medusa,
        ]
        solver = Solver.from_csv(file, strategies)

    def test_3d_medusa_rule_3(self) -> None:
        # Given
        file = os.path.dirname(data.__file__) + "\\test_3d_medusa_rule_3.csv"
        strategies = [
            IntersectionRemoval,
            NakedCandidates,
            HiddenCandidates,
            XCycles,
            D3Medusa,
        ]
        solver = Solver.from_csv(file, strategies)

        # When
        solved = solver._solve()

        # Then
        assert solved is True

    def test_3d_medusa_rule_4(self) -> None:
        # Given
        file = os.path.dirname(data.__file__) + "\\test_3d_medusa_rule_4.csv"
        strategies = [
            IntersectionRemoval,
            NakedCandidates,
            HiddenCandidates,
            XYChains,
            D3Medusa,
        ]
        solver = Solver.from_csv(file, strategies)

        # When
        solved = solver._solve()

        # Then
        assert solved is True

    def test_3d_medusa_rule_5(self) -> None:
        # Given
        file = os.path.dirname(data.__file__) + "\\test_3d_medusa_rule_5.csv"
        strategies = [
            IntersectionRemoval,
            NakedCandidates,
            HiddenCandidates,
            D3Medusa,
        ]
        solver = Solver.from_csv(file, strategies)

        # When
        solved = solver._solve()

        # Then
        assert solved is True

    def test_3d_medusa_rule_6(self) -> None:
        # Given
        file = os.path.dirname(data.__file__) + "\\test_3d_medusa_rule_6.csv"
        strategies = [
            IntersectionRemoval,
            NakedCandidates,
            HiddenCandidates,
            D3Medusa,
        ]
        solver = Solver.from_csv(file, strategies)

        # When
        solved = solver._solve()

        # Then
        assert solved is True
