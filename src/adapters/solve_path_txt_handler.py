from pathlib import Path

from src.domain.ports.solve_path_handler_interface import SolvePathHandlerInterface
from src.domain.solve_path import SolvePath


class SolvePathTxtHandler(SolvePathHandlerInterface):
    def save(self, solve_path: SolvePath, name: str | Path) -> None:
        filename = f"{name}_solve_path.txt"
        with open(filename, "w") as file:
            for step_count, step in enumerate(solve_path.path):
                file.write(f"\n# STEP: {step_count + 1}\n")
                for update in step:
                    file.write(f"  - {update}")
            file.write("\n--END--")
