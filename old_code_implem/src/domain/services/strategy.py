from src.domain.models.sudoku import Sudoku


class Strategy:
    def __init__(self, sudoku: Sudoku) -> None:
        self.sudoku = sudoku

    def __call__(self, *args, **kwargs) -> Sudoku:
        self.execute()
        return self.sudoku

    def execute(self) -> None:
        raise NotImplemented
