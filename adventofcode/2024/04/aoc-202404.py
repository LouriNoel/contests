import os
import sys

from utils.sylis import read, findall_chunk_in_grid, rotate_array2d_clockwise, build_wordseek_chunks

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

XMAS_patterns = build_wordseek_chunks("XMAS")

cross_MAS_patterns: list[list[str]] = [
    [
        "M.S",
        ".A.",
        "M.S"
    ]
]
for _ in range(3):
    cross_MAS_patterns.append(rotate_array2d_clockwise(cross_MAS_patterns[-1]))

if star != 2:
    count = sum(len(findall_chunk_in_grid(lines, pattern)) for pattern in XMAS_patterns)
    print(f" *: {count}")

if star != 1:
    count = sum(len(findall_chunk_in_grid(lines, pattern)) for pattern in cross_MAS_patterns)
    print(f"**: {count}")
