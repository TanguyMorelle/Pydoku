import itertools
from collections.abc import Iterator, Sequence

from pydoku.domain.models.types import Position


def get_visibility(position: Position) -> Sequence[Position]:
    u, v = 3 * (position[0] // 3), 3 * (position[1] // 3)
    rows = [(row, position[1]) for row in range(9)]
    columns = [(position[0], column) for column in range(9)]
    blocks = [(u + i, v + j) for i in range(3) for j in range(3)]
    return list(set(rows + columns + blocks) - {position})


def get_block(position: Position) -> int:
    return 3 * (position[0] // 3) + position[1] // 3


def get_subsets[T](elements: list[T], *, max_size=None) -> Iterator[list[list[T]]]:
    for size in range(2, max_size or len(elements)):
        yield list(itertools.combinations(elements, size))
