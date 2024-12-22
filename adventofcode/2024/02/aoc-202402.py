import os
import sys

from utils.sylis import read, numbers

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

def is_safe(levels: list[int]) -> bool:
    #differences = [b - a for a, b in zip(levels[:-1], levels[1:])]
    differences = [levels[i] - levels[i-1] for i in range(1, len(levels))]
    return ((all(delta >= 0 for delta in differences) or all(delta <= 0 for delta in differences))
            and all(delta != 0 and abs(delta) <= 3 for delta in differences))

def is_damp(report: list[int]) -> bool:
    for i in range(len(report)):
        damp = report.copy()
        damp.pop(i)
        if is_safe(damp):  # check if the report is safe when removing the i-th element, for any i
            return True
    return False


reports = [numbers(line) for line in lines]
safeness = [is_safe(report) for report in reports]

if star != 2:
    safe_count = safeness.count(True)
    print(f" *: {safe_count}")

if star != 1:
    safe_or_damp_count = sum(1 for i, report in enumerate(reports) if safeness[i] or is_damp(report))
    print(f"**: {safe_or_damp_count}")
