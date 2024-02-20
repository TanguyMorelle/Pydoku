from src.utils.types import Position


def get_visibility(position: Position) -> list[Position]:
    u, v = 3 * (position[0] // 3), 3 * (position[1] // 3)
    rows = [(row, position[1]) for row in range(9)]
    columns = [(position[0], column) for column in range(9)]
    blocks = [(u + i, v + j) for i in range(3) for j in range(3)]
    return list(set(rows + columns + blocks) - {position})
