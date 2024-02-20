from argparse import ArgumentParser


def get_argument_parser() -> ArgumentParser:
    arg_parser = ArgumentParser(description="Pydoku")
    arg_parser.add_argument(
        "--file",
        "-f",
        type=str,
        help="Path to the csv file containing the sudoku",
    )
    arg_parser.add_argument(
        "--seq",
        "-s",
        type=str,
        help="sequence of 81 characters representing the sudoku",
    )
    return arg_parser
