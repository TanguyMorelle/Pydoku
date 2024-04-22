import itertools
from typing import Iterator, TypeVar

from src.common.types import Position

T = TypeVar("T")


def get_visibility(position: Position) -> list[Position]:
    u, v = 3 * (position[0] // 3), 3 * (position[1] // 3)
    rows = [(row, position[1]) for row in range(9)]
    columns = [(position[0], column) for column in range(9)]
    blocks = [(u + i, v + j) for i in range(3) for j in range(3)]
    return list(set(rows + columns + blocks) - {position})


def get_block(position: Position) -> int:
    return 3 * (position[0] // 3) + position[1] // 3


def get_subsets(elements: list[T]) -> Iterator[list[tuple[T]]]:
    for size in range(2, len(elements)):
        yield list(itertools.combinations(elements, size))
