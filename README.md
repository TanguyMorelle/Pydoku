# Pydoku: Python Sudoku Solver with human reach techniques
![CI](https://github.com/TanguyMorelle/Pydoku/actions/workflows/ci.yml/badge.svg?branch=master)
![Coverage](https://img.shields.io/endpoint?url=https://TanguyMorelle.github.io/Pydoku/coverage.json)

Most techniques implemented originate or are inspired from Andrew Stuart's
great [website](https://www.sudokuwiki.org/sudoku.htm).

---
## Installation

The project requires `just` to run, you can install it with
```console
sudo apt install just
```
<br>

---
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
<br>
<br>

---
## Currently Implemented Techniques

### Base

✅ 0: Basic Sudoku Rules (Hidden singles)

### Level 1

✅ 1: Naked Sets<br>
✅ 2: Hidden Sets<br>
❌ 3: Pointing Pairs<br>
❌ 4: Box/Line Reduction<br>

### Level 2

❌ 5: X-Wing<br>
❌ 6: Simple Colouring<br>
❌ 7: Y-Wing<br>
❌ 8: Swordfish<br>
❌ 9: XYZ Wing<br>
❌ 10: BUG<br>
❌ 11: Avoidable Rectangles

### Level 3

❌ 12-a: X-Chains<br>
❌ 12-b: X-Cycles<br>
❌ 13: XY-Chain<br>
❌ 14: 3D Medusa<br>
❌ 15: Jellyfish<br>
❌ 16: Unique Rectangles<br>
❌ 17: Fireworks<br>
❌ 18: SK Loops<br>
❌ 19: Extended Unique Rect.<br>
❌ 20: Hidden Unique Rect's<br>
❌ 21: WXYZ Wing<br>
❌ 22: Aligned Pair Exclusion

### Level 4

❌ 23: Exocet<br>
❌ 24: Grouped X-Cycles<br>
❌ 25: Empty Rectangles<br>
❌ 26: Finned X-Wing<br>
❌ 27: Finned Swordfish<br>
❌ 28a: Inference Chains<br>
❌ 28b: AIC with Groups<br>
❌ 28c: AIC with ALSs<br>
❌ 29: Sue-De-Coq<br>
❌ 30: Digit Forcing chains<br>
❌ 31: Nishio Forcing Chains<br>
❌ 32: Cell Forcing Chains<br>
❌ 33: Unit Forcing Chains<br>
❌ 34: Almost Locked Sets<br>
❌ 35: Death Blossom<br>
❌ 36: Pattern Overlay
