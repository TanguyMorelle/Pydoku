from argparse import ArgumentParser

from src.adapters.sudoku_csv_handler import SudokuCsvHandler
from src.adapters.sudoku_seq_handler import SudokuSeqHandler
from src.domain.sudoku import Sudoku


class PydokuParser(ArgumentParser):
    def __init__(self) -> None:
        super().__init__(description="Pydoku")
        self._setup()

    def _setup(self) -> None:
        self.add_argument(
            "--file", "-f", type=str, help="Path to the csv file containing the sudoku"
        )
        self.add_argument(
            "--seq",
            "-s",
            type=str,
            help="sequence of 81 characters representing the sudoku",
        )


def get_sudoku(params: list[str]) -> Sudoku:
    parser = PydokuParser()
    args = parser.parse_args(params)
    if filename := args.file:
        if not filename.endswith(".csv"):
            parser.error("file format not supported")
        return SudokuCsvHandler().load(filename)
    if seq := args.seq:
        return SudokuSeqHandler().load(seq)
    parser.error("Please kprovide a file or a sequence")
