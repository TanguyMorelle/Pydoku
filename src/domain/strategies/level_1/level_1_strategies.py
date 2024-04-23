from src.domain.strategies.level_1.hidden_candidates import HiddenCandidates
from src.domain.strategies.level_1.naked_candidates import NakedCandidates
from src.domain.strategies.strategy_level import StrategyLevel


class Level1Strategies(StrategyLevel):
    HIDDEN_CANDIDATES = HiddenCandidates
    NAKED_CANDIDATES = NakedCandidates
