import os
import re
import sys

from utils.sylis import read

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

patterns1 = [
    ["XMAS"],
    [
        "X...",
        ".M..",
        "..A.",
        "...S",
    ],
    [
        "X",
        "M",
        "A",
        "S",
    ],
    [
        "...X",
        "..M.",
        ".A..",
        "S...",
    ],
    ["SAMX"],
    [
        "S...",
        ".A..",
        "..M.",
        "...X",
    ],
    [
        "S",
        "A",
        "M",
        "X",
    ],
    [
        "...S",
        "..A.",
        ".M..",
        "X...",
    ]
]

patterns2 = [
    [
        "M.S",
        ".A.",
        "M.S"
    ],
    [
        "M.M",
        ".A.",
        "S.S"
    ],
    [
        "S.M",
        ".A.",
        "S.M"
    ],
    [
        "S.S",
        ".A.",
        "M.M"
    ]
]


def findall_pattern_in_grid(grid: list[str], sub: list[str], unused: str = "§") -> list[tuple[int, int]]:
    # to ensure that a line match does not wrap, we must add an unused character at the end of each line

    w, sub_w = len(grid[0]), len(sub[0])
    dw = w - sub_w
    length_pattern = ".{" + str(dw+1) + "}" # +1 to account for the added separator at each EOL

    matched_indexes = []

    row_grid = unused.join(grid)
    row_pattern = re.compile(length_pattern.join(sub))
    # cannot use re.finditer because it does not allow overlapping matches
    start = 0
    while (m := row_pattern.search(row_grid, start)) is not None:
        i = m.start()
        x, y = i % w, i // w
        matched_indexes.append((x, y))
        start = i+1

    return matched_indexes


if star != 2:
    indexes = []
    for i, pattern in enumerate(patterns1):
        indexes.extend((i, x, y) for x, y in findall_pattern_in_grid(lines, pattern))
    print(f" *: {len(indexes)}")

if star != 1:
    indexes = []
    for i, pattern in enumerate(patterns2):
        indexes.extend((i, x, y) for x, y in findall_pattern_in_grid(lines, pattern))
    print(f"**: {len(indexes)}")
