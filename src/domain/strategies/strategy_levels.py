from enum import Enum
from typing import Iterator, Type

from src.domain.strategies.base.base_strategies import BaseStrategies
from src.domain.strategies.level_1.level_1_strategies import Level1Strategies
from src.domain.strategies.strategy import Strategy


class StrategyLevels(Enum):
    BASE = BaseStrategies
    LEVEL_1 = Level1Strategies

    @classmethod
    def strategies(cls) -> Iterator[Type[Strategy]]:
        for obj in cls:
            for strategy in obj.value.values():
                yield strategy
