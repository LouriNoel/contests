import os
import sys

from utils.sylis import read

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

w, h = len(lines[0]), len(lines)

def find_antennas(grid: list[str]) -> dict[str, list[tuple[int, int]]]:
    """ Find the position of all antennas of the same frequency. """
    antennas: dict[str, list[tuple[int, int]]] = {}
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c != ".":
                if c not in antennas:
                    antennas[c] = []
                antennas[c].append((x, y))
    return antennas

antennas_per_frequency = find_antennas(lines)  # frequency -> list of positions (x,y)


def count_antinodes(harmonics: bool):
    antennas_field = [["." for x in range(w)] for y in range(h)]
    for frequency, antennas in antennas_per_frequency.items():
        pairs = [(a, b) for a in antennas for b in antennas if a != b]  # also remove single antenna
        for (x1, y1), (x2, y2) in pairs:
            dx, dy = x2 - x1, y2 - y1

            i, j = 0, 0
            if not harmonics:
                i, j = 1, 1

            while 0 <= x1 - i * dx < w and 0 <= y1 - i * dy < h:
                antennas_field[y1 - i*dy][x1 - i*dx] = "#"
                i += 1
                if not harmonics:
                    break

            while 0 <= x2 + j * dx < w and 0 <= y2 + j * dy < h:
                antennas_field[y2 + j*dy][x2 + j*dx] = "#"
                j += 1
                if not harmonics:
                    break

    result = sum(1 for row in antennas_field for c in row if c == "#")
    print(result)


if star != 2:
    count_antinodes(False)

if star != 1:
    count_antinodes(True)
