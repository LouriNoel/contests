import os
import sys

from utils.sylis import read, digits

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

heights = [digits(line) for line in read(filepath)]


def walk(grid: list[list[int]], x: int, y: int) -> list[list[tuple[int, int]]]:
    """ Return a list of valid hiking trails starting from (x,y). """
    w, h, height = len(grid[0]), len(grid), grid[y][x]
    if height == 9:
        return [[(x, y)]]

    paths: list[list[tuple[int, int]]] = []
    neighbours = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]
    for x2, y2 in neighbours:
        if 0 <= x2 < w and 0 <= y2 < h and grid[y2][x2] == height+1:
            for path in walk(grid, x2, y2):
                path.insert(0, (x, y))
                paths.append(path)
    return paths  # can return empty list


def get_all_hiking_trails(grid: list[list[int]]) -> list[list[tuple[int, int]]]:
    hiking_trails = []
    for y, row in enumerate(grid):
        for x, height in enumerate(row):
            if height == 0:
                hiking_trails.extend(walk(grid, x, y))

    return hiking_trails


def get_sum_of_scores(hiking_trails: list[list[tuple[int, int]]]) -> int:
    ends_per_trailhead = {}
    for path in hiking_trails:
        start, end = path[0], path[-1]
        if start not in ends_per_trailhead:
            ends_per_trailhead[start] = []
        if end not in ends_per_trailhead[start]:  # do not count duplicate ends / multiple paths leading to the same end
            ends_per_trailhead[start].append(end)
    return sum(len(li) for li in ends_per_trailhead.values())


hiking_trails = get_all_hiking_trails(heights)

if star != 2:
    result = get_sum_of_scores(hiking_trails)
    print(f" *: {result}")

if star != 1:
    # Each hiking trail is already distinct, so we just need to count them
    # (instead of doing a sum of ratings per trailhead)
    result = len(hiking_trails)
    print(f"**: {result}")
