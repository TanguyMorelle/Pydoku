import re

import numpy as np

from src.domain.sudoku import Sudoku
from src.utils.updates import Update


class DataLoader:
    @staticmethod
    def from_csv(filename: str) -> Sudoku:
        data = np.genfromtxt(filename, delimiter=",")
        return Sudoku(data)

    @staticmethod
    def from_sequence(sequence: str) -> Sudoku:
        formatted_sequence = re.sub(r"\D", "0", sequence)
        data = np.array([int(char) for char in formatted_sequence]).reshape(9, 9)
        return Sudoku(data)

    @staticmethod
    def save_grid(sudoku: Sudoku, name: str) -> None:
        filename = f"{name}_result.csv" if name else "result.csv"
        np.savetxt(filename, sudoku.grid.astype(int), delimiter=",", fmt="%.1s")

    @staticmethod
    def save_solve_path(solve_path: list[list[Update]], name: str) -> None:
        filename = f"{name}_solve_path.txt" if name else "solve_path.txt"
        with open(filename, "w") as file:
            for step_count, step in enumerate(solve_path):
                file.write(f"\n# STEP: {step_count + 1}\n")
                for update in step:
                    file.write(f"  - {update}")
            file.write("\n--END--")
