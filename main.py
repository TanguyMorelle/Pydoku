from src.domain.data_loader import DataLoader
from src.domain.solver import Solver
from src.domain.sudoku import Sudoku
from src.utils.argument_parser import get_argument_parser


def load_sudoku() -> Sudoku:
    parser = get_argument_parser()
    args = parser.parse_args()
    if filename := args.file:
        if not filename.endswith(".csv"):
            parser.error("file format not supported")
        return DataLoader.from_csv(args.file)
    if args.seq:
        return DataLoader.from_sequence(args.seq)
    parser.error("Please provide a file or a sequence")


if __name__ == "__main__":
    sudoku = load_sudoku()
    solver = Solver(sudoku)
    solver.solve()
