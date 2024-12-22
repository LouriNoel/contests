import os
import sys

from utils.sylis import read, numbers

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

def is_safe(levels: list[int]) -> bool:
    """ Check if a report is safe. """
    deltas = [levels[i] - levels[i - 1] for i in range(1, len(levels))]
    min_delta, max_delta = min(deltas), max(deltas)
    # `min_delta * max_delta > 0` checks for both sign equality and "at least 1" requirement
    return min_delta * max_delta > 0 and min_delta >= -3 and max_delta <= 3

def is_damp(levels: list[int]) -> bool:
    """ Check if a report is safe when ignoring one of its levels. """
    # check if the report is safe when removing the i-th element, for any i
    return any(is_safe(levels[:i] + levels[i+1:]) for i in range(len(levels)))

reports = [numbers(line) for line in lines]
safeness = [is_safe(report) for report in reports]

if star != 2:
    safe_count = safeness.count(True)
    print(f" *: {safe_count}")

if star != 1:
    safe_or_damp_count = sum(1 for i, report in enumerate(reports) if safeness[i] or is_damp(report))
    print(f"**: {safe_or_damp_count}")
