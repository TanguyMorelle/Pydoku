# Pydoku: Python Sudoku Solver with human reach techniques

[![CI](https://img.shields.io/github/actions/workflow/status/TanguyMorelle/Pydoku/tests.yml?branch=master&logo=github&label=Tests)](https://github.com/pydantic/pydantic/actions?query=event%3Apush+branch%3Amaster+workflow%3ATests)
[![Coverage](https://coverage-badge.samuelcolvin.workers.dev/TanguyMorelle/Pydoku.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/TanguyMorelle/Pydoku)

---

Most technique implemented originate or are inspired from Andrew Stuart's
great [website](https://www.sudokuwiki.org/sudoku.htm).

## Installation

```console
bash scripts/setup.sh
```

## Usage

For more information on how to use the solver run:

```console
python main.py --help
```

## Supported input formats

- **csv file**<br>
  9x9 grid with 0 or for empty cells, ',' separated


- **sequence**<br>
  81 characters long string with any non digit char for empty cells

## Output

- **solve path**<br>
  text file containing the different updates applied to the grid


- **csv file** (if csv input)<br>
  9x9 grid with the solution or the state of the grid if in a locked state


- **sequence** (if sequence input)<br>
  81 characters long string with the solution or the state of the grid if in a locked state

## Currently Implemented Techniques

### Base

- [x] 0: Basic Sudoku Rules

### Level 1

- [ ] 1: Hidden Singles
- [ ] 2: Naked Pairs/Triples
- [ ] 3: Hidden Pairs/Triples
- [ ] 4: Naked/Hidden Quads
- [ ] 5: Pointing Pairs
- [ ] 6: Box/Line Reduction

### Level 2

- [ ] 7: X-Wing
- [ ] 8: Simple Colouring
- [ ] 9: Y-Wing
- [ ] 10: Swordfish
- [ ] 11: XYZ Wing
- [ ] 12: BUG
- [ ] 13: Avoidable Rectangles

### Level 3

- [ ] 14-a: X-Chains
- [ ] 14-b: X-Cycles
- [ ] 15: XY-Chain
- [ ] 16: 3D Medusa
- [ ] 17: Jellyfish
- [ ] 18: Unique Rectangles
- [ ] 19: Fireworks
- [ ] 20: SK Loops
- [ ] 21: Extended Unique Rect.
- [ ] 22: Hidden Unique Rect's
- [ ] 23: WXYZ Wing
- [ ] 24: Aligned Pair Exclusion

### Level 4

- [ ] 25: Exocet
- [ ] 26: Grouped X-Cycles
- [ ] 27: Empty Rectangles
- [ ] 28: Finned X-Wing
- [ ] 29: Finned Swordfish
- [ ] 30a: Inference Chains
- [ ] 30b: AIC with Groups
- [ ] 30c: AIC with ALSs
- [ ] 31: Sue-De-Coq
- [ ] 32: Digit Forcing chains
- [ ] 33: Nishio Forcing Chains
- [ ] 34: Cell Forcing Chains
- [ ] 35: Unit Forcing Chains
- [ ] 36: Almost Locked Sets
- [ ] 37: Death Blossom
- [ ] 38: Pattern Overlay
