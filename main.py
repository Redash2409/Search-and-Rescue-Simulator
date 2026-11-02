import random
import heapq

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
def print_grid(grid, drone=None, target=None, path=None):

    # Convert the route into a set
    if path is not None:
        path_cells = set(path)
    else:
        path_cells = set()

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

            elif position in path_cells:
                symbol = "*"

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
    explored_count = 0

    # Up, down, left and right
    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    while queue:

        current = queue.popleft()
        explored_count += 1

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
        return None, explored_count

    # Reconstruct the route
    path = []

    current = target

    while current != start:

        path.append(current)

        current = parent[current]

    path.append(start)

    path.reverse()

    return path, explored_count

# 8. MANHATTAN DISTANCE HEURISTIC
def manhattan_distance(position, target):

    return abs(position[0] - target[0]) + abs(position[1] - target[1])

# 9. A* PATHFINDING
def astar(grid, start, target):

    start = tuple(start)
    target = tuple(target)

    # Priority queue stores estimated total cost, current cost and position
    open_heap = []

    start_distance = manhattan_distance(start, target)

    heapq.heappush(open_heap, (start_distance, 0, start))

    # Store the previous cell for each discovered position
    parent = {}

    # Store the shortest known distance from the start
    g_score = {start: 0}
    explored_count = 0

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    while open_heap:

        estimated_cost, current_cost, current = heapq.heappop(open_heap)

        # Ignore an outdated entry in the priority queue
        if current_cost != g_score.get(current):
            continue
        explored_count += 1

        # Check whether the target has been reached
        if current == target:

            path = []
            position = target

            while position != start:
                path.append(position)
                position = parent[position]

            path.append(start)
            path.reverse()

            return path, explored_count

        # Explore neighbouring cells
        for dr, dc in directions:

            new_r = current[0] + dr
            new_c = current[1] + dc

            if not is_valid_move(grid, new_r, new_c):
                continue

            new_position = (new_r, new_c)

            # Each movement has a cost of 1
            new_cost = current_cost + 1

            if new_cost < g_score.get(new_position, float("inf")):

                parent[new_position] = current

                g_score[new_position] = new_cost

                estimated_total = (
                    new_cost + manhattan_distance(new_position, target)
                )

                heapq.heappush(
                    open_heap,
                    (estimated_total, new_cost, new_position)
                )

    return None, explored_count

# 10. MAIN PROGRAM
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

    # Calculate routes using both algorithms
    bfs_path, bfs_explored = bfs(grid, drone, target)
    astar_path, astar_explored = astar(grid, drone, target)

    # Display BFS results
    print("\nBFS RESULTS")
    print("Cells explored:", bfs_explored)

    if bfs_path is None:
        print("No route found.")

    else:
        print("BFS found a route!")
        print("Number of movements:", len(bfs_path) - 1)

    # Display A* results
    print("\nA* RESULTS")
    print("Cells explored:", astar_explored)

    if astar_path is None:
        print("No route found.")

    else:
        print("A* found a route!")
        print("Number of movements:", len(astar_path) - 1)

    # Display only one grid, showing the A* route
    print("\nSearch area (* = A* route):")
    print_grid(grid, drone, target, astar_path)

# RUN THE PROGRAM
if __name__ == "__main__":
    main()