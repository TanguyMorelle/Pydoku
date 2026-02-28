from typing import overload, Any


class Cell:
    def __init__(self, line: int, column: int, values: tuple[int]) -> None:
        self.line = line
        self.column = column
        self.values = values

    @property
    def position(self) -> tuple[int, int]:
        return self.line, self.column

    @overload
    def check_visibility(self, cell: tuple[int, int]) -> bool:
        ...

    @overload
    def check_visibility(self, cell: "Cell") -> bool:
        ...

    def check_visibility(self, cell: "Cell") -> bool:
        if isinstance(cell, Cell):
            y_pos, x_pos = cell.line, cell.column
        else:
            y_pos, x_pos = cell
        if self.line == y_pos or self.column == x_pos:
            return True
        if self.line // 3 == y_pos // 3 and self.column // 3 == x_pos // 3:
            return True
        return False

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Cell):
            return (
                self.line == other.line and
                self.column == other.column
            )
        return False

    def __hash__(self):
        return hash((self.line, self.column))
