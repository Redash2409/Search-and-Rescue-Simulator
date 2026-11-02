# Search-and-Rescue Route Planner

## Overview

This Python program simulates a drone finding a route across a randomly generated 10 x 10 grid. It compares two pathfinding algorithms, Breadth-First Search (BFS) and A*.

The target coordinates are generated and given to both algorithms. The program demonstrates route planning to a known target; it does not detect people or search an unknown area.

## Run

Run the program from this folder:

```bash
python main.py
```

The program uses only the Python standard library. No additional packages are needed.

## What it does

Each run:

1. Creates a 10 x 10 grid and places 10 to 16 randomly selected obstacles.
2. Places the drone at `(0, 0)` and selects a free cell as the target.
3. Runs BFS and A* on the same grid and reports each algorithm's explored-cell count, execution time, and route length when a route is found.
4. Displays the grid with the A* route.

Movement is limited to up, down, left, and right, and each move has the same cost. BFS finds a shortest route for equal-cost moves. A* uses Manhattan distance to guide its search.

## Grid symbols

- `D` — drone start
- `T` — target
- `#` — obstacle
- `*` — cells along the A* route
- `.` — open cell

The random map may have no route to the target. In that case, the program reports that no route was found.

## Limitations

- The target location is known to the route planners; there is no camera, person detection, or probability map.
- The grid does not model real terrain, flight physics, or different movement costs.
- Execution time varies with the computer and system load. Treat it as an approximate measurement, not a stable benchmark.
