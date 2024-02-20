import numpy as np

EMPTY_GRID = np.zeros((9, 9), dtype=int)

EASY_GRID = np.array(
    [
        [3, 0, 0, 9, 6, 7, 0, 0, 1],
        [0, 4, 0, 3, 0, 2, 0, 8, 0],
        [0, 2, 0, 0, 0, 0, 0, 7, 0],
        [0, 7, 0, 0, 0, 0, 0, 9, 0],
        [0, 0, 0, 8, 7, 3, 0, 0, 0],
        [5, 0, 0, 0, 1, 0, 0, 0, 3],
        [0, 0, 4, 7, 0, 5, 1, 0, 0],
        [9, 0, 5, 0, 0, 0, 2, 0, 7],
        [8, 0, 0, 6, 2, 1, 0, 0, 4],
    ]
)

EASY_GRID_POSSIBLE_VALUES = np.array(
    [
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 1, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        [
            [1, 0, 0, 0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 1],
        ],
        [
            [1, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 1, 1],
            [1, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 1, 1, 1, 1, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 1],
        ],
        [
            [1, 1, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 1, 0, 1, 0],
        ],
        [
            [1, 1, 0, 1, 0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 0, 0, 0, 1, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [1, 1, 0, 1, 1, 1, 0, 0, 0],
            [0, 1, 0, 0, 1, 1, 0, 0, 0],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 1],
            [0, 1, 0, 0, 0, 1, 0, 1, 1],
            [0, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 1],
            [0, 0, 0, 1, 0, 1, 1, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        [
            [0, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 1],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0, 1],
            [0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
    ]
)

EASY_GRID_SOLVED = np.array(
    [
        [3, 5, 8, 9, 6, 7, 4, 2, 1],
        [7, 4, 1, 3, 5, 2, 6, 8, 9],
        [6, 2, 9, 1, 8, 4, 3, 7, 5],
        [1, 7, 3, 5, 4, 6, 8, 9, 2],
        [4, 9, 2, 8, 7, 3, 5, 6, 1],
        [5, 8, 6, 2, 9, 1, 7, 4, 3],
        [2, 6, 4, 7, 3, 5, 1, 9, 8],
        [9, 3, 7, 4, 1, 8, 2, 5, 6],
        [8, 1, 5, 6, 2, 9, 7, 3, 4],
    ]
)
