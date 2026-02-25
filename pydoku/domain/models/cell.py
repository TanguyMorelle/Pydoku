from collections.abc import Sequence
from typing import Any, Self

from pydantic import BaseModel

from pydoku.domain.models.types import Position
from pydoku.utils.grid_tools import get_block, get_visibility


class Cell(BaseModel):
    row: int
    column: int
    values: list[int] | None = None

    @property
    def position(self) -> Position:
        return self.row, self.column

    @property
    def block(self) -> int:
        return get_block(self.position)

    @property
    def visibility(self) -> Sequence[Position]:
        return get_visibility(self.position)

    def transpose(self) -> Self:
        self.row, self.column = self.column, self.row
        return self

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Cell):
            raise TypeError(f"Cannot compare Cell with {type(other)}")
        return self.position < other.position

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cell):
            return False
        return self.position == other.position and sorted(self.values or []) == sorted(
            other.values or []
        )

    def __hash__(self) -> int:
        return hash((self.row, self.column, self.values))
