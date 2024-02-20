import sys

from src.domain.solver import Solver
from src.utils.argument_parser import get_sudoku

if __name__ == "__main__":
    sudoku = get_sudoku(sys.argv[1:])
    solver = Solver(sudoku)
    solver.solve()
