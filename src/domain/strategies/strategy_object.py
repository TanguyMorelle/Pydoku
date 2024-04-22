from abc import ABC, abstractmethod


class StrategyObject(ABC):
    @abstractmethod
    def realign(self) -> "StrategyObject": ...
