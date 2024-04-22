from typing import Any

from src.domain.strategies.strategy_object import StrategyObject


def fake_strategy_object_factory() -> StrategyObject:
    class FakeStrategyObject(StrategyObject):
        def __init__(self) -> None:
            self.realign_call_count = 0

        def realign(self) -> "StrategyObject":
            self.realign_call_count += 1
            return self

        def __str__(self) -> str:
            return "[UNKNOWN] FakeStrategyObject\n"

    return FakeStrategyObject()
