import os
import sys

from utils.sylis import read

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

DIRS = ["^", ">", "v", "<"]
INCRS = {
    "^": (0, -1),
    ">": (+1, 0),
    "v": (0, +1),
    "<": (-1, 0)
}

def move(grid, W, H, x, y, d):
    """ Make the guard move forward once, or turn in-place once if an obstacle is in the way. """

    dx, dy = INCRS[d]
    right = (DIRS.index(d) + 1) % 4

    if 0 <= x+dx < W and 0 <= y+dy < H and grid[y+dy][x+dx] == "#":
        return x, y, DIRS[right]
    else:
        return x+dx, y+dy, d


def previous_position(x, y, d):
    # previous position, and turn right
    right = (DIRS.index(d) + 1) % 4
    opposite = (DIRS.index(d) + 2) % 4
    dx, dy = INCRS[DIRS[opposite]]
    return x+dx, y+dy, DIRS[right]


grid = [[c for c in line] for line in lines]
W, H = len(grid[0]), len(grid)

# Find the guard's position and direction
x, y = [(px, py) for py, row in enumerate(grid) for px, c in enumerate(row) if c not in ".#"][0]
d = grid[y][x]  # ^ > v <

# Initial values
x0, y0, d0 = x, y, d


# Make the guard move a first time until they leave the area
path: list[tuple[int, int, str]] = []
candidates: set[tuple[int, int]] = set()
while 0 <= x < W and 0 <= y < H:
    if (x, y) not in candidates:
        path.append((x, y, d))  # save the first time this position is reached
    candidates.add((x, y))

    x, y, d = move(grid, W, H, x, y, d)


if star != 2:
    print(f" *:{len(candidates)}")


if star != 1:
    # 1. The initial position (x0,y0) is not required to be part of a loop
    # 2. An obstacle is only useful when placed on the original path (to make it deviate)
    # 3. Do not walk through the original path everytime an obstacle is tried, that would be a lot of useless iterations

    # We cannot place an obstacle on the guard's initial position
    path.pop(0)
    candidates.remove((x0, y0))

    nb_loops = 0
    for ox, oy, od in path:
        # Try to place an obstacle at each position on the original path of the guard, then search for a loop.
        # Each position in `path` also have a direction, which can be reversed to find the previous position,
        # where no wall could have been.
        print(f"- ({ox}, {oy}, {od})")

        grid[oy][ox] = "#"
        x, y, d = previous_position(ox, oy, od)  # start just before the newly placed obstacle

        visited = []
        while 0 <= x < W and 0 <= y < H:
            x, y, d = move(grid, W, H, x, y, d)
            if (x, y, d) in visited:
                nb_loops += 1
                print(f"loop found! count={nb_loops}, ox={ox}, oy={oy}")
                break
            visited.append((x, y, d))

        # Remove the obstacle for the next try
        grid[oy][ox] = "."

    print(f"**:{nb_loops}")
