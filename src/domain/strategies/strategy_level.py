from enum import Enum

from src.domain.strategies.strategy import Strategy


class StrategyLevel(Enum):
    @classmethod
    def values(cls) -> list[type[Strategy]]:
        return [obj.value for obj in cls]
