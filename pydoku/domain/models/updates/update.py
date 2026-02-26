from abc import ABC, abstractmethod


class Update[T](ABC):
    @abstractmethod
    def realign(self) -> T: ...

    @abstractmethod
    def transpose(self) -> T: ...


class GridUpdate[T](Update[T], ABC): ...


class OptionsUpdate[T](Update[T], ABC): ...
