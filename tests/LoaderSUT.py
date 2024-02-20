import os

import tests.fixtures.grids.csv as csv_grids


class LoaderSUT:
    @staticmethod
    def get_grid(filename: str) -> str:
        return os.path.join(os.path.dirname(csv_grids.__file__), filename)
