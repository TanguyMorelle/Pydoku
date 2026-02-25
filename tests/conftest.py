import pytest

from tests.fixtures.sudoku_test_builder import SudokuTestBuilder


@pytest.fixture
def sudoku_builder() -> SudokuTestBuilder:
    return SudokuTestBuilder()
