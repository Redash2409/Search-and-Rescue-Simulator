import random

from collections import deque

# CONSTANTS
SIZE = 10
DRONE_START = (0, 0)
MIN_OBSTACLES = 10
MAX_OBSTACLES = 16


# 1. CREATE THE GRID
def create_grid():
    grid = []

    for i in range(SIZE):
        row = []

        for j in range(SIZE):
            row.append(".")

        grid.append(row)

    return grid


# 2. ADD RANDOM OBSTACLES
def add_obstacles(grid):
    obstacle_count = random.randint(
        MIN_OBSTACLES, MAX_OBSTACLES
    )

    obstacle_positions = set()

    while len(obstacle_positions) < obstacle_count:

        r = random.randint(0, SIZE - 1)
        c = random.randint(0, SIZE - 1)

        position = (r, c)

        if position != DRONE_START:
            obstacle_positions.add(position)

    for r, c in obstacle_positions:
        grid[r][c] = "#"

    return obstacle_count


# 3. FIND AN EMPTY CELL FOR THE TARGET
def get_random_empty_cell(grid, reserved=None):

    if reserved is None:
        reserved = set()

    empty_cells = []

    for r in range(len(grid)):
        for c in range(len(grid[0])):

            if grid[r][c] == "." and (r, c) not in reserved:
                empty_cells.append((r, c))

    if not empty_cells:
        raise ValueError("No empty cells available.")

    return list(random.choice(empty_cells))


# 4. DISPLAY THE GRID
def print_grid(grid, drone=None, target=None):

    drone_pos = tuple(drone) if drone is not None else None
    target_pos = tuple(target) if target is not None else None

    for r in range(len(grid)):
        symbols = []

        for c in range(len(grid[0])):
            position = (r, c)

            if position == drone_pos:
                symbol = "D"

            elif position == target_pos:
                symbol = "T"

            else:
                symbol = grid[r][c]

            symbols.append(symbol)

        print(" ".join(symbols))


# 5. CHECK WHETHER A MOVE IS VALID
def is_valid_move(grid, r, c):

    if r < 0 or r >= len(grid):
        return False

    if c < 0 or c >= len(grid[0]):
        return False

    if grid[r][c] == "#":
        return False

    return True


# 6. MOVE THE DRONE
def move_drone(drone, grid, dr, dc):

    new_r = drone[0] + dr
    new_c = drone[1] + dc

    if is_valid_move(grid, new_r, new_c):

        drone[0] = new_r
        drone[1] = new_c

        return True

    return False

# 7. BREADTH-FIRST SEARCH
def bfs(grid, start, target):

    queue = deque()

    visited = set()

    parent = {}

    start = tuple(start)
    target = tuple(target)

    queue.append(start)
    visited.add(start)

    # Up, down, left and right
    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    while queue:

        current = queue.popleft()

        # Check whether target is found
        if current == target:
            break

        # Investigate neighbouring cells
        for dr, dc in directions:

            new_r = current[0] + dr
            new_c = current[1] + dc

            if not is_valid_move(grid, new_r, new_c):
                continue

            new_position = (new_r, new_c)

            if new_position in visited:
                continue

            visited.add(new_position)

            parent[new_position] = current

            queue.append(new_position)

    # Check whether a route exists
    if target not in visited:
        return None

    # Reconstruct the route
    path = []

    current = target

    while current != start:

        path.append(current)

        current = parent[current]

    path.append(start)

    path.reverse()

    return path

# 8. MAIN PROGRAM
def main():

    # Call the grid creation function
    grid = create_grid()

    # Generate obstacles
    obstacle_count = add_obstacles(grid)

    # Set drone starting position
    drone = list(DRONE_START)

    # Place target in an empty cell
    target = get_random_empty_cell(
        grid,
        reserved={tuple(drone)}
    )

    # Display everything
    print("SEARCH AND RESCUE SIMULATOR")
    print("---------------------------")
    print("Grid size:", SIZE, "x", SIZE)
    print("Obstacles:", obstacle_count)
    print("Drone position:", drone)
    print("Target position:", target)
    print()

    # Calculate the route using BFS
    path = bfs(grid, drone, target)

    if path is None:
        print("No route found.")
    else:
        print("\nBFS found a route!")
        print("Route:", path)
        print("Number of movements:", len(path) - 1)
        print("\nSearch area:")
        print_grid(grid, drone, target)


# RUN THE PROGRAM
if __name__ == "__main__":
    main()