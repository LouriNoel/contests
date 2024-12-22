import os
import sys

from utils.sylis import read

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

DIRS = {"^": "UP",
        ">": "RIGHT",
        "v": "DOWN",
        "<": "LEFT"}


def move(grid, x, y, d):
    # Move or turn once

    W, H = len(grid[0]), len(grid)

    if d == "UP":
        if y != 0 and grid[y-1][x] == "#":
            d = "RIGHT"
            grid[y][x] = ">"
        else:
            y = y-1
            if y > 0:
                grid[y][x] = "^"

    elif d == "RIGHT":
        if x != W-1 and grid[y][x+1] == "#":
            d = "DOWN"
            grid[y][x] = "v"
        else:
            x = x+1
            if x < W:
                grid[y][x] = ">"

    elif d == "DOWN":
        if y != H-1 and grid[y+1][x] == "#":
            d = "LEFT"
            grid[y][x] = "<"
        else:
            y = y+1
            if y < H:
                grid[y][x] = "v"

    elif d == "LEFT":
        if x != 0 and grid[y][x-1] == "#":
            d = "UP"
            grid[y][x] = "^"
        else:
            x = x-1
            if x > 0:
                grid[y][x] = "<"

    return x, y, d


def star1():
    grid = [[c for c in line] for line in lines]
    W, H = len(grid[0]), len(grid)

    # find the guard's position and direction
    x, y = [(px, py) for py, row in enumerate(grid) for px, c in enumerate(row) if c not in ".#"][0]
    d = DIRS[grid[y][x]]

    # Make the guard move until they leave the area
    while 0 <= x < W and 0 <= y < H:
        x, y, d = move(grid, x, y, d)

    count = sum(1 for row in grid for c in row if c not in ".#")
    print(f" *:{count}")


# Takes too long, but still gives the right result
def star2():
    grid = [[c for c in line] for line in lines]
    W, H = len(grid[0]), len(grid)

    # find the guard's position and direction
    x, y = [(px, py) for py, row in enumerate(grid) for px, c in enumerate(row) if c not in ".#"][0]
    d = DIRS[grid[y][x]]

    x0, y0, d0, c0 = x, y, d, grid[y][x]

    candidates = []
    G = [[c for c in row] for row in grid]  # modifiable copy

    # Make the guard move a first time
    while 0 <= x < W and 0 <= y < H:
        x, y, d = move(G, x, y, d)
        candidates = [(_x, _y) for _y, _row in enumerate(G) for _x, _c in enumerate(_row) if _c not in ".#"]
        candidates.remove((x0, y0))

    # An obstacle is only useful when placed on the original path (to make it deviate)

    count = 0
    for ox, oy in candidates:
        print(f"- ({ox}, {oy})")

        grid[oy][ox] = "#"
        x, y, d = x0, y0, d0

        visited = []
        while 0 <= x < W and 0 <= y < H:
            x, y, d = move(grid, x, y, d)
            if (x, y, d) in visited:
                count += 1
                print(f"loop found! count={count}, ox={ox}, oy={oy}")
                break
            visited.append((x, y, d))

        # clear
        grid[oy][ox] = "."
        for _y, _row in enumerate(grid):
            for _x, _c in enumerate(_row):
                if _c not in ".#":
                    grid[_y][_x] = "."
        grid[y0][x0] = c0

    print(f"**:{count}")


star1()
star2()
