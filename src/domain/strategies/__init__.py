from enum import Enum
from typing import Iterator, Type

from src.domain.strategies.base import BaseStrategies
from src.domain.strategies.strategy import Strategy
from src.domain.strategies.strategy_level import StrategyLevel


class StrategyLevels(Enum):
    BASE = BaseStrategies

    @classmethod
    def values(cls) -> list[type[StrategyLevel]]:
        return [obj.value for obj in cls]

    @classmethod
    def strategies(cls) -> Iterator[Type[Strategy]]:
        for obj in cls:
            for strategy in obj.value.values():
                yield strategy
