import os
import sys

from utils.sylis import read

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

XMAS = "XMAS"
INCR = [-1, 0, 1]

def check_once(grid, x, y, dx, dy):
    # Check the "XMAS" word on the (dx, dy) direction
    nX, nY = len(grid[0]), len(grid)
    for i, c in enumerate(XMAS):
        X, Y = x+dx*i, y+dy*i
        if X < 0 or Y < 0 or X >= nX or Y >= nY:
            return False
        if grid[y+dy*i][x+dx*i] != c:
            return False
    return True

def check1(grid, x, y):
    found = []
    for dx in INCR:
        for dy in INCR:
            if not (dx == 0 and dy == 0):
                # Check the "XMAS" word on the 8 directions
                if check_once(grid, x, y, dx, dy):
                    found.append((x, y, dx, dy))
    return found

def star1(grid):
    instances = []

    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == "X":
                instances.extend(check1(grid, x, y))

    print(len(instances))


if star != 2:
    star1(lines)


patterns = [
    [
        "M.S",
        ".A.",
        "M.S"
    ],
    [
        "S.S",
        ".A.",
        "M.M"
    ],
    [
        "S.M",
        ".A.",
        "S.M"
    ],
    [
        "M.M",
        ".A.",
        "S.S"
    ]
]

def check_pattern(grid, x, y, p):
    # Check if a pattern matches at position (x, y) on the grid
    for dy, pl in enumerate(p):
        for dx, c in enumerate(pl):
            if c != ".":
                if grid[y + dy][x + dx] != c:
                    return False
    return True

def check2(grid):
    count = 0
    for y in range(len(grid)-3+1):
        for x in range(len(grid[0])-3+1):
            # Check any of the four rotated "MAS" pattern on the whole grid
            for p in patterns:
                if check_pattern(grid, x, y, p):
                    count += 1
                    break
    return count


if star != 1:
    result = check2(lines)
    print(result)
