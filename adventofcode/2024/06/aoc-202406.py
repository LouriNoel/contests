import os
import sys

from utils.sylis import read

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)


def move(grid, x, y, d):
    """ Make the guard move forward once, or turn in-place once if an obstacle is in the way. """

    W, H = len(grid[0]), len(grid)

    if d == "^":
        if y != 0 and grid[y-1][x] == "#":
            d = ">"
            grid[y][x] = ">"
        else:
            y = y-1
            if y > 0:
                grid[y][x] = "^"

    elif d == ">":
        if x != W-1 and grid[y][x+1] == "#":
            d = "v"
            grid[y][x] = "v"
        else:
            x = x+1
            if x < W:
                grid[y][x] = ">"

    elif d == "v":
        if y != H-1 and grid[y+1][x] == "#":
            d = "<"
            grid[y][x] = "<"
        else:
            y = y+1
            if y < H:
                grid[y][x] = "v"

    elif d == "<":
        if x != 0 and grid[y][x-1] == "#":
            d = "^"
            grid[y][x] = "^"
        else:
            x = x-1
            if x > 0:
                grid[y][x] = "<"

    return x, y, d


grid = [[c for c in line] for line in lines]
W, H = len(grid[0]), len(grid)

# Find the guard's position and direction
x, y = [(px, py) for py, row in enumerate(grid) for px, c in enumerate(row) if c not in ".#"][0]
d = grid[y][x]  # ^ > v <

# Initial values
x0, y0, d0 = x, y, d


# Make the guard move a first time until they leave the area
candidates = set()
while 0 <= x < W and 0 <= y < H:
    candidates.add((x, y))
    x, y, d = move(grid, x, y, d)  # also write the path on the grid


if star != 2:
    print(f" *:{len(candidates)}")


if star != 1:
    # 1. The initial position (x0,y0) is not required to be part of a loop
    # 2. An obstacle is only useful when placed on the original path (to make it deviate)

    candidates.remove((x0, y0))  # we cannot place an obstacle on the guard's initial position

    nb_loops = 0
    for ox, oy in candidates:  # Try to place an obstacle at each position on the original path of the guard
        print(f"- ({ox}, {oy})")

        grid[oy][ox] = "#"
        x, y, d = x0, y0, d0

        visited = []
        while 0 <= x < W and 0 <= y < H:
            x, y, d = move(grid, x, y, d)
            if (x, y, d) in visited:
                nb_loops += 1
                print(f"loop found! count={nb_loops}, ox={ox}, oy={oy}")
                break
            visited.append((x, y, d))

        # Remove the obstacle for the next try
        grid[oy][ox] = "."

    print(f"**:{nb_loops}")
