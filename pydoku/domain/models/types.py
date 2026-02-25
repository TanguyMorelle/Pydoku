import numpy as np
from jaxtyping import Int

type Array9 = Int[np.ndarray, "9"]
type Array9x9 = Int[np.ndarray, "9 9"]
type Array9x9x9 = Int[np.ndarray, "9 9 9"]
type Array3x3 = Int[np.ndarray, "3 3"]
type Array3x3x9 = Int[np.ndarray, "3 3 9"]

type Grid = Array9 | Array3x3
type Options = Array9 | Array9x9 | Array3x3x9

type Position = tuple[int, int]
