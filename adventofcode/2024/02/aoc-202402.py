import os
import sys

from utils.sylis import read

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

reports = [[int(x) for x in line.split()] for line in lines]

def check(report):
    diffs = [report[i+1] - report[i] for i in range(len(report)-1)]
    a = [abs(x) for x in diffs]
    # check if all differences are positive or negative, and their absolute value is within the acceptable range
    return (all(x >= 0 for x in diffs) or all(x <= 0 for x in diffs)) and min(a) >= 1 and max(a) <= 3

safe_reports = [r for r in reports if check(r)]
print(f" *: {len(safe_reports)}")

def check_damp(report):
    if check(report):  # already safe
        return True
    for i in range(len(report)):
        damp = report.copy()
        damp.pop(i)
        if check(damp):  # check if the report is safe when removing the i-th element, for any i
            return True
    return False

damp_safe_reports = [r for r in reports if check_damp(r)]
print(f"**: {len(damp_safe_reports)}")
