from typing import Any, Optional

from src.common.types import Position
from src.utils.grid_tools import get_block, get_visibility


class Cell:
    def __init__(
        self, row: int, column: int, values: Optional[tuple[int, ...]] = None
    ) -> None:
        self.row = row
        self.column = column
        self.values = tuple(sorted(values or []))

    @property
    def position(self) -> Position:
        return self.row, self.column

    @property
    def block(self) -> int:
        return get_block(self.position)

    @property
    def visibility(self) -> list[Position]:
        return get_visibility(self.position)

    def transpose(self) -> "Cell":
        return Cell(self.column, self.row, self.values)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Cell):
            return False
        return self.__dict__ == other.__dict__

    def __lt__(self, other: "Cell") -> bool:
        return self.position <= other.position

    def __hash__(self) -> int:
        return hash((self.row, self.column, self.values))
