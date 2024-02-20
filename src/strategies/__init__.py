from enum import Enum

from src.strategies.base import BaseStrategies
from src.utils.strategy_level import StrategyLevel


class StrategyLevels(Enum):
    BASE = BaseStrategies

    @classmethod
    def values(cls) -> list[type[StrategyLevel]]:
        return [obj.value for obj in cls]
