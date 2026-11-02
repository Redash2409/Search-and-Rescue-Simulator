# Autonomous Search-and-Rescue Route Planner

## Overview

This Python project models a small search-and-rescue navigation problem on a 2D grid. A drone starts at a base and must reach a reported target location while avoiding blocked cells. It compares two path-planning algorithms:

- **Breadth-First Search (BFS):** explores cells in increasing numbers of moves and finds a shortest route when every move has equal cost.
- **A\* (A-star):** prioritises cells using `f(n) = g(n) + h(n)`, where `g(n)` is the cost already travelled and `h(n)` is the Manhattan-distance estimate to the target.

**Scope clarification:** in this version, the target's coordinates are supplied to the route planner. The program investigates autonomous route planning to a reported location. It does not yet use a camera, detect a person, or model a drone searching an unknown area.

## Requirements

- Python 3.10 or newer (Python 3.13 is suitable).
- The core simulator uses only Python's standard library. No extra packages are needed to run `main.py`.
- Matplotlib is needed only to create a graph from the experiment results.

Install Matplotlib (optional):

```bash
python -m pip install matplotlib
```

On Windows, if `python` does not select the Store installation, try:

```bash
py -3.13 -m pip install matplotlib
```

## Run the simulator

Open a terminal in this folder and run:

```bash
python main.py
```

On Windows, you can also use:

```bash
py -3.13 main.py
```

Choose:

1. Run one mission and view the routes found by BFS and A*.
2. Run repeated experiments on the same maps for both algorithms and save raw measurements to `results.csv`.
3. Exit.

## Create a graph

After running option 2:

```bash
python plot_results.py
```

This creates `algorithm_comparison.png`, comparing the average number of expanded cells at different obstacle densities. The graph combines the tested grid sizes, so it should be treated as an overview. For a more detailed investigation, analyse each grid size separately.

## Experimental method

The experiment varies:

- Grid sizes: 10 x 10, 15 x 15 and 20 x 20.
- Obstacle densities: 10%, 20% and 30%.
- Repeated trials: 30 maps for each size-density combination.

Both algorithms receive the exact same generated map in each trial. This makes the comparison fairer. The random sequence is seeded so the experiment can be repeated.

Measurements include:

- Whether a route was found.
- Route length in moves.
- Number of cells expanded.
- Search execution time in milliseconds.

Execution time is affected by computer load and is often very small for these maps. Use averages over many trials and place more emphasis on expanded cells and path length.

## Limitations and future improvements

- All moves have equal cost; forest, water and steep terrain are not modelled yet.
- The target location is known to the planner. A future version could simulate a hidden target and a drone camera/search pattern.
- The model is a 2D grid, not a real flight or physics simulation.
- The probability-based search strategy is not yet implemented.
- The experiment is a simplified model and should not be presented as evidence of real-world drone performance.

## Suggested research question

**How does obstacle density affect the search effort and route length of BFS and A* in a grid-based autonomous navigation simulation?**

A further extension could investigate whether a probability map helps an agent prioritise areas when the target location is unknown.
