from collections import deque
from typing import Any

Position = tuple[int, int]


class XCycle(deque):
    def __init__(self, sequence: list[Position]) -> None:
        super().__init__(sequence)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, XCycle):
            reversed_loop = other.reverse()
            for i in range(len(self)+1):
                self.rotate()
                if other == self or other == reversed_loop:
                    self.rotate(-i)
                    return True
        return False
