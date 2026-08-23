import random

size = 10
grid = []
for i in range(size):
    row = []
    for j in range(size):
        row.append(".")
    grid.append(row)
def print_grid(grid):
    for row in grid:
        print(" ".join(row))


obstacle = random.randint(0,16)
for i in range(obstacle):
    add_obstacles = [
    random.randint(0, size -1),
    random.randint(0, size -1)
                    ]
    grid[add_obstacles[0]][add_obstacles[1]] = "#"

drone = [0,0]
def is_valid_move(grid, r, c):
    if r < 0 or r >= len(grid):
        return False
    if c < 0 or c >= len(grid):
        return False
    if grid[r][c] == "#":
        return False
    return True
def move_drone(drone, grid, dr, dc):
    new_r = drone[0] + dr
    new_c = drone[1] + dc

    if is_valid_move(grid, new_r, new_c):
        drone[0] = new_r
        drone[1] = new_c
grid[drone[0]][drone[1]] = "D"

target = [
    random.randint(0, size -1),
    random.randint(0, size -1)
]
grid[target[0]][target[1]] = "T"

print_grid(grid)
